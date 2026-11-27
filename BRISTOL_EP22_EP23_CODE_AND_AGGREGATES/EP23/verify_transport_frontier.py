#!/usr/bin/env python3
"""Post-hoc fixed-state transport frontier. Input: private EP20/EP22 replay states.
No test targets enter the analysis. Output is private aggregate evidence + checks.
The ridge-ball result assumes exact stationarity; report residual-adjusted upper
bounds and test the direct unshifted objective on every constructed witness.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import argparse, json, hashlib
from pathlib import Path
import numpy as np, pandas as pd
from scipy.linalg import cholesky,solve_triangular
from scipy.optimize import linprog,minimize
ETA=.01
GUARD=1e-8

def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def qp_screen(A,g):
 # Boundary minimum in whitened coordinates, with a strict-interior starting point.
 B=np.vstack([A,-A]); m,q=B.shape
 lp=linprog(np.r_[np.zeros(q),1.],A_ub=np.vstack([np.column_stack([B,np.zeros(m)]),np.column_stack([np.eye(q),-np.ones(q)]),np.column_stack([-np.eye(q),-np.ones(q)])]),b_ub=np.r_[np.ones(m),np.zeros(2*q)],A_eq=np.r_[g,0.][None,:],b_eq=[1.0001],bounds=[(None,None)]*q+[(0,None)],method='highs')
 assert lp.success,lp.message
 start=lp.x[:-1]/(g@lp.x[:-1]); assert max(abs(A@start))<1-1e-6
 fit=minimize(lambda x:.5*x@x,start,jac=lambda x:x,constraints=[{'type':'eq','fun':lambda x:g@x-1,'jac':lambda x:g},{'type':'ineq','fun':lambda x:1-B@x,'jac':lambda x:-B}],method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
 assert fit.success,fit.message
 x=fit.x; l=float(fit.multipliers[0]); mu=np.maximum(fit.multipliers[1:],0)
 # Weak-duality certificate valid for any nonnegative mu, unconstrained l.
 dual=2*l-2*mu.sum()-np.linalg.norm(B.T@mu-l*g)**2
 # Enforce exact equality algebraically; blend toward strict interior to cover small numerical excess.
 x=x+(1-g@x)*g/(g@g)
 x=(1-1e-8)*x+1e-8*start; x=x/(g@x)
 assert abs(g@x-1)<1e-10 and max(abs(A@x))<=1+1e-10
 primal=x@x
 assert dual>0 and abs(dual-primal)<1e-7
 # Independent dual re-evaluation in raw linear algebra is done by caller.
 return float(dual),float(primal),l,mu,x

def audit(results,out):
 out.mkdir(parents=True,exist_ok=True); folds=[];screens=[]; hashes=[]; cert={}; rowcount=0;direct_count=0; max_station=0.; max_replay=0.
 for sp in sorted(results.glob('*/state.npz')):
  fold=sp.parent.name; hashes.append({'fold':fold,'sha256':sha(sp)});z=np.load(sp,allow_pickle=False)
  P,Pt,b=z['P'],z['Pt'],z['beta']; n,q=P.shape;y=z['ytrain']-float(z['offset']);lam=float(z['lam']);assert lam>0
  H=P.T@P/n+lam*np.eye(q);J=float(np.mean((P@b-y)**2)+lam*b@b);r=H@b-P.T@y/n
  L=cholesky(H,lower=True); M=solve_triangular(L.T,np.eye(q),lower=False); A=P@M; T=Pt@M
  delta_station=np.linalg.norm(M.T@r); R0=np.sqrt(ETA*J); Rshift=np.sqrt(ETA*J+delta_station**2)+delta_station
  max_station=max(max_station,float(max(abs(r))))
  if fold.startswith('LOGO'):
   # Test the set of design rows directly, no input labels or targets required.
   train_rows=set(map(tuple,P));assert all(tuple(row) in train_rows for row in Pt)
   folds.append(dict(fold=fold,test_rows=len(Pt),status='REDUNDANT_ALL_POSITIVE_EPSILON',frontier_stationary_dB=0.,lower_guard_dB=0.,upper_guard_dB=0.,exact_matches=len(Pt),direct_witness_rows_at_0p1=0,universal_at_0p1=True,universal_at_1=True,stationarity_inf=float(max(abs(r)))))
   continue
  # Unconstrained minimizer of boundary energy: M g/||g||^2.
  v=np.einsum('ij,ij->i',T,T);assert np.min(v)>0
  ratios=np.max(np.abs(A@T.T),axis=0)/v
  caps=R0*np.sqrt(v);good=ratios<1-1e-9;assert good.any()
  k=int(np.argmax(np.where(good,caps,-np.inf)));critical=float(caps[k]);g=T[k];baseline=float(1/v[k]);
  # Boundary minimizer has a strict train margin. It gives a lower critical threshold.
  assert ratios[k]<1-1e-9
  # Screen all rows not already below the controlling threshold by ridge-only upper bound.
  row_upper=Rshift*np.sqrt(v); todo=np.flatnonzero(caps>critical+1e-10)
  for j in todo:
   dual,primal,l,mu,x=qp_screen(A,T[j]); B=np.vstack([P,-P]); w=B.T@mu-l*Pt[j]
   direct_dual=2*l-2*mu.sum()-w@np.linalg.solve(H,w)
   assert abs(direct_dual-dual)<1e-8
   safe_dual=min(dual,direct_dual)-1e-10*max(1.,abs(dual));assert safe_dual>baseline
   row_upper[j]=Rshift/np.sqrt(safe_dual)
   screens.append(dict(fold=fold,local_test_row=int(j),ridge_only_upper_dB=float(caps[j]),boundary_energy_primal=primal,boundary_energy_dual_safe=safe_dual,transport_upper_dB=float(row_upper[j]),controlling_dB=critical,dual_replay_difference=float(abs(direct_dual-dual))))
   cert[f'{fold}_screen{j}_mu']=mu;cert[f'{fold}_screen{j}_lambda']=np.array(l);cert[f'{fold}_screen{j}_v']=x
  max_upper=float(max(row_upper)); assert max_upper<=critical+GUARD/2,(fold,critical,max_upper)
  # Construct each direct direction at epsilon=0.1, with a 1e-7 safety contraction.
  unit=T.T/np.sqrt(v); train_norm=np.max(abs(A@unit),axis=0)
  scale=np.minimum(R0,.1/np.maximum(train_norm,1e-300))*(1-1e-7)
  D=(M@unit)*scale
  # choose sign to ensure the first-order residual cannot increase the objective
  signs=np.where(r@D>0,-1.,1.); D*=signs
  actual=np.abs(np.einsum('ij,ji->i',Pt,D)); valid=actual>.1+1e-9
  for j in np.flatnonzero(valid):
   d=D[:,j]; tr=float(max(abs(P@d))); cost=float((np.mean((P@(b+d)-y)**2)+lam*((b+d)@(b+d))-J)/J)
   assert tr<.1 and cost<ETA and abs(Pt[j]@d)>.1+1e-9
   max_replay=max(max_replay,abs(cost-(d@H@d+2*r@d)/J))
  # A strict witness very close to frontier, not only at epsilon=.1.
  e_low=critical-GUARD; target=(critical+e_low)/2
  d=M@(g/v[k])*target
  if r@d>0:d=-d
  tr=float(max(abs(P@d))); test=float(max(abs(Pt@d))); deltaJ=float((np.mean((P@(b+d)-y)**2)+lam*((b+d)@(b+d))-J)/J)
  assert tr<e_low and test>e_low+1e-10 and deltaJ<ETA
  assert max_upper<critical+GUARD
  cert[f'{fold}_frontier_witness']=d;cert[f'{fold}_frontier_control']=np.array(k);cert[f'{fold}_direct_witness_indices']=np.flatnonzero(valid);cert[f'{fold}_direct_witness_deltas']=D[:,valid].T
  # At 1 dB even the residual-adjusted pure objective ball implies all held-out constraints.
  assert max(Rshift*np.sqrt(v))<1
  direct_count+=int(valid.sum());rowcount+=len(Pt)
  folds.append(dict(fold=fold,test_rows=len(Pt),status='POSITIVE_CRITICAL_THRESHOLD',frontier_stationary_dB=critical,lower_guard_dB=e_low,upper_guard_dB=critical+GUARD,exact_matches=0,controlling_train_to_test_ratio=float(ratios[k]),screened_candidates=len(todo),direct_witness_rows_at_0p1=int(valid.sum()),max_direct_witness_test_dB=float(max(actual)),pure_ridge_upper_at_1_dB=float(max(Rshift*np.sqrt(v))),near_frontier_witness_train_dB=tr,near_frontier_witness_test_dB=test,near_frontier_witness_relative_objective=deltaJ,universal_at_0p1=False,universal_at_1=True,stationarity_inf=float(max(abs(r)))))
 assert len(folds)==9 and rowcount==372 and direct_count==180 and len(screens)==4
 pd.DataFrame(folds).to_csv(out/'frontier_fold_summary.csv',index=False);pd.DataFrame(screens).to_csv(out/'screening_certificates_PRIVATE.csv',index=False)
 np.savez_compressed(out/'witnesses_PRIVATE.npz',**cert)
 report={'status':'PASS','eta':ETA,'folds':len(folds),'LOGO_exact_redundancy_rows':sum(x['exact_matches'] for x in folds),'NACA0012_rows':rowcount,'NACA0012_direct_violation_rows_at_0p1':direct_count,'nonredundant_fold_budget_sets':sum(not x['universal_at_0p1'] for x in folds),'redundant_fold_budget_sets':sum(x['universal_at_0p1']+x['universal_at_1'] for x in folds),'screened_QP_candidates':len(screens),'max_stationarity_inf':max_station,'max_direct_objective_replay_error':max_replay,'numerical_guard_dB':GUARD,'source_states':hashes,'scope':'Post hoc fixed-premise finite held-out design; no held-out targets, refitting, coefficient sign claim, or population guarantee. Frontier values exact in ideal stationary model up to certified numerical brackets, not interval arithmetic.'}
 (out/'QA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='source_states'},indent=2));print(pd.DataFrame(folds).to_string(index=False));print(pd.DataFrame(screens).to_string(index=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();audit(a.results,a.out)
