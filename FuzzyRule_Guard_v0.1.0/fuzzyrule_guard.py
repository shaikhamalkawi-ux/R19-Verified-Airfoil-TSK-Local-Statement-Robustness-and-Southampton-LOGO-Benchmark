#!/usr/bin/env python3
"""Research prototype: finite-input sign audit for frozen first-order ridge TSK.
Requires NumPy and SciPy. Uses float64 bounds and checked witnesses; unresolved
is a legitimate outcome. Never certifies physical correctness or domain transfer.
"""
import argparse, csv, hashlib, io, json, math, os, re, zipfile
from collections import Counter
from pathlib import Path

# Keep the numerical work reproducible and avoid BLAS thread oversubscription.
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import linprog, minimize

VERSION = '0.1.0'
GUARD = 1e-8
AF4_SHA256 = "1edd543fb6544f8bd23de418b3108f1617518251bf35a2cb18ec966d5a7225dd"

class Model:
    def __init__(self, z):
        self.P = np.asarray(z['P'], dtype=float)
        self.b = np.asarray(z['beta'], dtype=float)
        self.y = np.asarray(z['ytrain'], dtype=float)-float(z['offset'])
        self.lam = float(z['lam'])
        self.Pt = np.asarray(z['Pt'], dtype=float) if 'Pt' in z else None
        if self.P.ndim != 2 or self.b.ndim != 1 or self.y.ndim != 1:
            raise ValueError('P must be 2D; beta and ytrain must be 1D')
        self.n,self.q=self.P.shape
        if not self.n or not self.q or self.b.shape!=(self.q,) or self.y.shape!=(self.n,):
            raise ValueError('incompatible or empty arrays')
        if self.Pt is not None and (self.Pt.ndim!=2 or self.Pt.shape[1]!=self.q or not len(self.Pt)):
            raise ValueError('Pt must be nonempty and have the same columns as P')
        if not all(np.all(np.isfinite(x)) for x in [self.P,self.b,self.y]+([] if self.Pt is None else [self.Pt])) or not math.isfinite(self.lam) or self.lam<=0:
            raise ValueError('finite inputs and positive ridge lambda required')
        residual=self.P@self.b-self.y
        self.J=float(residual@residual/self.n+self.lam*(self.b@self.b))
        if not math.isfinite(self.J) or self.J<=0: raise ValueError('positive finite reference objective required')
        self.H=self.P.T@self.P/self.n+self.lam*np.eye(self.q)
        self.C=cho_factor(self.H,lower=True)
        self.g=self.P.T@residual/self.n+self.lam*self.b
        self.center=-self.solve(self.g)
        # The exact objective-increase set is an ellipsoid centered at -H^-1 g.
        # This correction also accounts for a nonzero finite-precision gradient.
        self.gHg=float(-self.g@self.center)
        if not np.all(np.isfinite(self.center)) or self.gHg < -GUARD:
            raise ValueError('invalid ridge objective geometry')
        self.A=np.vstack((self.P,-self.P))
    def solve(self,c): return cho_solve(self.C,c)
    def ellipse_upper(self,c,eta):
        c=np.asarray(c,dtype=float)
        v=float(c@self.solve(c)); rad2=eta*self.J+max(0.,self.gHg)
        if not math.isfinite(v) or v < -GUARD: raise ValueError('invalid ellipsoid quadratic form')
        return float(c@self.center)+math.sqrt(max(0.,v)*rad2)
    def upper(self,c,eps,eta,mu=None):
        u=self.ellipse_upper(c,eta)
        if mu is not None:
            mu=np.asarray(mu,dtype=float)
            if mu.shape!=(2*self.n,) or not np.all(np.isfinite(mu)): raise ValueError('invalid dual array')
            mu=np.maximum(mu,0.)
            # For every feasible d, c.d <= eps*sum(mu) + support_ellipsoid(c-A^T mu).
            # No exact LP stationarity or full-column-rank assumption is required.
            v=eps*float(mu.sum())+self.ellipse_upper(c-self.A.T@mu,eta)
            u=min(u,v)
        return u+GUARD*(1+abs(u)+float(np.linalg.norm(c))*float(np.linalg.norm(self.b)))
    def check(self,c,base,d,eps,eta,gamma):
        d=np.asarray(d,dtype=float)
        if d.shape!=self.b.shape or not np.all(np.isfinite(d)): return None
        move=float(c@d); train=float(np.max(np.abs(self.P@d)))
        alt=self.b+d; r=self.P@alt-self.y
        direct=float((r@r/self.n+self.lam*(alt@alt)-self.J)/self.J)
        quad=float((d@self.H@d+2*self.g@d)/self.J)
        # Use both the direct objective and the quadratic expression. Strict sign
        # and requested magnitude are verified to an explicit float64 tolerance.
        t=GUARD*(1+base)
        if not all(math.isfinite(v) for v in (move,train,direct,quad)) or abs(direct-quad)>GUARD*(1+abs(quad)):
            return None
        if train>eps or max(direct,quad)>eta or move<=base+t or move<(1+gamma)*base-t:
            return None
        test=None if self.Pt is None else float(np.max(np.abs(self.Pt@d)))
        if test is not None and not math.isfinite(test): return None
        return dict(max_training_change=train,relative_objective_increase=direct,
                    quadratic_objective_increase=quad,heldout_max_change=test,
                    heldout_budget_retained=None if test is None else test<=eps,
                    alternative_beta=alt.tolist(),delta=d.tolist())
    def functional(self,j):
        if not 0<=j<self.q: raise ValueError('coefficient index out of range')
        b=float(self.b[j]);c=np.zeros(self.q);c[j]=-np.sign(b)
        return b,c


def budgets(eps,eta,gamma):
    if not all(map(math.isfinite,(eps,eta,gamma))) or eps<=0 or eta<=0 or gamma<=0:
        raise ValueError('epsilon, eta and gamma must be positive finite values')


def row(m,j,eps,eta,gamma):
    b,c=m.functional(j)
    return dict(index=j,original_coefficient=b,epsilon=eps,eta=eta,gamma=gamma,
                status='UNRESOLVED',method='none'),b,c


def certify_saved(m,j,eps,eta,gamma,mu=None,d=None):
    """Recheck existing witnesses and duals without trusting stored class labels."""
    r,b,c=row(m,j,eps,eta,gamma)
    if abs(b)<=GUARD: return r
    bound=m.upper(c,eps,eta,mu)
    r['movement_upper_bound']=bound
    if bound<abs(b):
        r.update(status='PROTECTED',method='ellipsoid_or_corrected_linear_dual',zero_margin=abs(b)-bound,dual_mu=None if mu is None else np.maximum(mu,0.).tolist())
        return r
    if d is not None:
        w=m.check(c,abs(b),d,eps,eta,gamma)
        if w is not None: r.update(status='REVERSIBLE',method='checked_witness',**w)
    return r


def audit(m,j,eps,eta,gamma):
    """Generate a new certificate/witness or explicitly abstain."""
    budgets(eps,eta,gamma)
    r,b,c=row(m,j,eps,eta,gamma)
    if abs(b)<=GUARD: return r
    base=abs(b); u=m.upper(c,eps,eta)
    r['movement_upper_bound']=u
    if u<base:
        r.update(status='PROTECTED',method='ellipsoid',zero_margin=base-u);return r
    # LP supplies a candidate dual; its residual is corrected by the ellipsoid.
    lp=linprog(-c,A_ub=m.A,b_ub=np.full(2*m.n,eps),bounds=[(None,None)]*m.q,method='highs')
    if lp.success:
        mu=-np.asarray(lp.ineqlin.marginals)
        u=m.upper(c,eps,eta,mu);r['movement_upper_bound']=u
        if u<base:
            r.update(status='PROTECTED',method='corrected_linear_dual',zero_margin=base-u,dual_mu=np.maximum(mu,0.).tolist());return r
    # Use a slightly stronger crossing target and slightly tighter input budget
    # to avoid calling a rounded boundary value feasible.
    target=(1+gamma)*base+GUARD*(1+base)
    hc=m.solve(c);den=float(c@hc)
    if den<=0: return r
    dc=m.center+hc*((target-c@m.center)/den)
    candidates=[dc]
    if lp.success and float(c@lp.x)>target:
        candidates.append(lp.x*(target/float(c@lp.x)))
    for d in candidates:
        w=m.check(c,base,d,eps,eta,gamma)
        if w is not None:
            r.update(status='REVERSIBLE',method='checked_direct_candidate',**w);return r
    # Cutting-plane convex QP. Only accepted via a full-input witness check;
    # solver termination, or failure to find a witness, is never a protection proof.
    d=candidates[-1]; tight=eps*(1-1e-7)
    ix=np.unique(np.argsort(-np.abs(m.P@d))[:min(32,m.n)])
    def obj(x): return float((x@m.H@x+2*m.g@x)/m.J)
    def grad(x): return 2*(m.H@x+m.g)/m.J
    for _ in range(20):
        V=m.P[ix]; B=np.vstack((V,-V))
        cons=[{'type':'eq','fun':lambda x: float(c@x-target),'jac':lambda x:c},
              {'type':'ineq','fun':lambda x:tight-B@x,'jac':lambda x:-B}]
        fit=minimize(obj,d,jac=grad,constraints=cons,method='SLSQP',options={'maxiter':200,'ftol':1e-11})
        d=np.asarray(fit.x)
        if not np.all(np.isfinite(d)): break
        w=m.check(c,base,d,eps,eta,gamma)
        if w is not None:
            r.update(status='REVERSIBLE',method='checked_qp_witness',**w);return r
        viol=np.flatnonzero(np.abs(m.P@d)>tight+GUARD*eps)
        new=np.setdiff1d(viol,ix)
        if not len(new): break
        new=new[np.argsort(-np.abs(m.P[new]@d))[:24]]
        ix=np.union1d(ix,new)
    return r


def model_indices(z,indices,block_size):
    q=len(z['beta'])
    if indices is not None:
        out=[int(x) for x in indices.split(',')]
    else:
        if block_size is None:
            if 'R' not in z: raise ValueError('provide --indices or --block-size; no rule layout metadata')
            R=int(z['R']);
            if R<=0 or q%R: raise ValueError('invalid R or coefficient ordering')
            block_size=q//R
        if block_size<2 or q%block_size: raise ValueError('invalid rule block size')
        out=[j for j in range(q) if j%block_size]
    if len(set(out))!=len(out) or not out or any(j<0 or j>=q for j in out): raise ValueError('invalid coefficient indices')
    return out


def digest(path):
    with open(path,'rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def replay_af4(path):
    """Verify the deposited 510 classifications using original dual/witness arrays.
    This does not redo the optimization, retrain, or recover missing historic bytes.
    """
    result=[]
    with zipfile.ZipFile(path) as arc:
        prefix='direct_derivative/inputs/'
        expected={}
        for r in csv.DictReader(io.StringIO(arc.read(prefix+'RESOLVED_510_STATEMENTS.csv').decode())):
            if float(r['epsilon'])==.1 and float(r['gamma'])==.001:
                key=(int(r['fold']),int(r['j']))
                if key in expected: raise ValueError('duplicate baseline row')
                expected[key]={'SIGN_PROTECTED_POINTWISE':'PROTECTED','FEASIBLE_REVERSAL':'REVERSIBLE'}[r['final_class']]
        if len(expected)!=510: raise ValueError('unexpected number of baseline rows')
        for fold in range(10):
            stem=f'AIRFOIL_ONESE_fold{fold:02d}'
            with np.load(io.BytesIO(arc.read(prefix+'states/'+stem+'.npz')),allow_pickle=False) as z, np.load(io.BytesIO(arc.read(prefix+'witnesses/'+stem+'_WITNESSES.npz')),allow_pickle=False) as w:
                m=Model(z);block=m.q//int(z['R'])
                for j in model_indices(z,None,block):
                    key=f'r{j//block:02d}_k{j%block}'
                    mu=w[key+'_lp_mu'].copy() # stored dual bounds +e_j; symmetry handles -e_j
                    if m.b[j]>0: mu=np.r_[mu[m.n:],mu[:m.n]]
                    wk=key+'_eps0.1_g0.001_d';d=w[wk] if wk in w else None
                    r=certify_saved(m,j,.1,.01,.001,mu,d)
                    r.update(fold=fold,expected=expected[(fold,j)],match=r['status']==expected[(fold,j)])
                    result.append(r)
    if len(result)!=510 or not all(r['match'] for r in result): raise ValueError('baseline verification mismatch')
    counts=Counter(r['status'] for r in result)
    if counts!={'PROTECTED':403,'REVERSIBLE':107}: raise ValueError('baseline counts mismatch')
    return result


def export(rows,output,metadata):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    summary={'version':VERSION,'scope':'fixed-antecedent finite-input numerical audit; not a physical/safety certificate',**metadata,'counts':dict(Counter(r['status'] for r in rows))}
    (output/'report.json').write_text(json.dumps({'summary':summary,'records':rows},indent=2,allow_nan=False)+'\n')
    keys=sorted(set().union(*(set(r)-{'alternative_beta','delta','dual_mu'} for r in rows)))
    with (output/'report.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    print(json.dumps(summary,indent=2,allow_nan=False))


def self_test():
    # Known identity-design protection and reversal, and an explicitly unresolved
    # zero coefficient. Also test held-out input checking independently of fitting.
    P=np.array([[1.,0.],[0.,1.]])
    b=np.array([1.,.1]);lam=.1;y=(1+2*lam)*b
    m=Model(dict(P=P,beta=b,ytrain=y,offset=0.,lam=lam,Pt=10*P))
    a=audit(m,0,.05,.5,.001);v=audit(m,1,.2,.5,.001)
    assert a['status']=='PROTECTED',a
    assert v['status']=='REVERSIBLE' and v['heldout_budget_retained'] is False,v
    m0=Model(dict(P=P,beta=np.array([1.,0.]),ytrain=np.array([1.2,0.]),offset=0.,lam=lam))
    assert audit(m0,1,.2,.5,.001)['status']=='UNRESOLVED'
    # Invalid lambda rejected.
    try: Model(dict(P=P,beta=b,ytrain=y,offset=0.,lam=0.))
    except ValueError: pass
    else: raise AssertionError('zero ridge was accepted')
    print('Self-test PASS: protection, reversal, held-out exceedance, zero coefficient abstention, invalid lambda rejection')


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('audit');a.add_argument('model');a.add_argument('--epsilon',type=float,required=True);a.add_argument('--eta',type=float,default=.01);a.add_argument('--gamma',type=float,default=.001);a.add_argument('--indices');a.add_argument('--block-size',type=int);a.add_argument('--out',default='guard_report')
    r=sub.add_parser('replay-af4');r.add_argument('archive');r.add_argument('--out',default='af4_readback')
    sub.add_parser('self-test')
    args=p.parse_args()
    if args.command=='self-test': self_test();return
    if args.command=='replay-af4':
        sha=digest(args.archive)
        if AF4_SHA256 is not None and sha!=AF4_SHA256: raise ValueError('AF4 source digest mismatch')
        rows=replay_af4(args.archive);export(rows,args.out,{'mode':'saved-certificate replay','input_sha256':sha,'matches':sum(r['match'] for r in rows),'total':len(rows)});return
    budgets(args.epsilon,args.eta,args.gamma)
    with np.load(args.model,allow_pickle=False) as z:
        m=Model(z);indices=model_indices(z,args.indices,args.block_size)
        rows=[audit(m,j,args.epsilon,args.eta,args.gamma) for j in indices]
    export(rows,args.out,{'mode':'fresh finite-input audit','input_sha256':digest(args.model),'max_reference_gradient':float(np.max(np.abs(m.g))),'total':len(rows)})

if __name__=='__main__':main()
