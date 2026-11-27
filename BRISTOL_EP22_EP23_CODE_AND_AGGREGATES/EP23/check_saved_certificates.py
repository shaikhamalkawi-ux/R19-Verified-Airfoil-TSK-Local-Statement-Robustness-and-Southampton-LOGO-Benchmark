#!/usr/bin/env python3
"""Optimizer-free independent check of saved EP23 certificates."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import argparse,hashlib,json
from pathlib import Path
import numpy as np,pandas as pd
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args();out=a.evidence
q=json.loads((out/'QA.json').read_text());folds=pd.read_csv(out/'frontier_fold_summary.csv').set_index('fold');screens=pd.read_csv(out/'screening_certificates_PRIVATE.csv');c=np.load(out/'witnesses_PRIVATE.npz',allow_pickle=False);expected={x['fold']:x['sha256'] for x in q['source_states']};nexact=nrows=ndirect=nscreen=nnear=0;eta=q['eta'];min_slack=np.inf
for sp in sorted(a.results.glob('*/state.npz')):
 f=sp.parent.name;assert hashlib.file_digest(sp.open('rb'),'sha256').hexdigest()==expected[f];rec=folds.loc[f];z=np.load(sp,allow_pickle=False);P,Pt,b=z['P'],z['Pt'],z['beta'];yc=z['ytrain']-z['offset'];lam=float(z['lam']);n,k=P.shape
 H=P.T@P/n+lam*np.eye(k);r=H@b-P.T@yc/n;J=lambda d:np.mean((P@(b+d)-yc)**2)+lam*np.sum((b+d)**2);J0=J(np.zeros(k));
 if f.startswith('LOGO'):
  for pt in Pt:assert np.any(np.all(P==pt,axis=1))
  assert rec.frontier_stationary_dB==0;nexact+=len(Pt);continue
 v=np.linalg.solve(H,Pt.T);row_energy=np.sum(Pt*v.T,axis=1);assert np.min(row_energy)>0
 residual_norm2=r@np.linalg.solve(H,r);radius=np.sqrt(eta*J0+residual_norm2)+np.sqrt(residual_norm2);upper=radius*np.sqrt(row_energy);assert upper.max()<1
 for row in screens[screens.fold==f].itertuples(index=False):
  j=int(row.local_test_row);mu=c[f'{f}_screen{j}_mu'];l=float(c[f'{f}_screen{j}_lambda']);assert np.all(mu>=0);B=np.vstack((P,-P));s=B.T@mu-l*Pt[j];dual=2*l-2*mu.sum()-s@np.linalg.solve(H,s);assert dual>0 and dual+1e-12>=row.boundary_energy_dual_safe;upper[j]=radius/np.sqrt(row.boundary_energy_dual_safe);nscreen+=1
 assert max(upper)<rec.upper_guard_dB
 d=c[f'{f}_frontier_witness'];idx=int(c[f'{f}_frontier_control']);assert max(abs(P@d))<rec.lower_guard_dB and abs(Pt[idx]@d)>rec.lower_guard_dB and (J(d)-J0)/J0<eta;nnear+=1
 assert abs(np.sqrt(eta*J0*row_energy[idx])-rec.frontier_stationary_dB)<1e-9
 ix=c[f'{f}_direct_witness_indices'];ds=c[f'{f}_direct_witness_deltas'];assert len(ix)==len(ds)==rec.direct_witness_rows_at_0p1 and len(set(ix))==len(ix)
 for j,d in zip(ix,ds):
  t=max(abs(P@d));cost=(J(d)-J0)/J0;test=abs(Pt[j]@d);assert t<.1 and cost<eta and test>.1;min_slack=min(min_slack,float(test-.1))
 ndirect+=len(ix);nrows+=len(Pt)
assert (nexact,nrows,ndirect,nscreen,nnear)==(1464,372,180,4,5)
res={'status':'PASS','optimizer_calls':0,'exact_row_checks':nexact,'heldout_upper_bound_rows':nrows,'direct_violations':ndirect,'QP_dual_replays':nscreen,'near_frontier_witnesses':nnear,'min_direct_test_excess_dB':min_slack,'source_states_sha256':len(expected)};(out/'INDEPENDENT_CERTIFICATE_QA.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
