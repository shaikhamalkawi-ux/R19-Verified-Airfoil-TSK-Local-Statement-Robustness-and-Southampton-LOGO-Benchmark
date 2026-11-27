#!/usr/bin/env python3
"""Check exact design-row containment and recompute aggregate paired contrasts.
Run only on private, reproduced EP20 output. No row-level outputs are exported.
"""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True)
d=pd.read_csv(a.results/'canonical_private.csv');x=d[['angle_deg','frequency_Hz']].to_numpy();rows=[]
for sp in sorted(a.results.glob('*/state.npz')):
 with np.load(sp,allow_pickle=False) as z:
  tr,te,P,Pt=z['tr'],z['te'],z['P'],z['Pt']; keys={tuple(x[i]):j for j,i in enumerate(tr)}
  match=[(j,keys[tuple(x[i])]) for j,i in enumerate(te) if tuple(x[i]) in keys];differences=[float(np.max(np.abs(Pt[j]-P[k]))) for j,k in match];exact=sum(np.array_equal(Pt[j],P[k]) for j,k in match)
  if sp.parent.name.startswith('LOGO'): assert len(te)==len(match)==exact and max(differences)==0
  else: assert len(match)==0
  rows.append(dict(fold=sp.parent.name,test_rows=len(te),matched=len(match),exact_design_rows=exact,max_design_difference=max(differences,default=None)))
assert len(rows)==9
pd.DataFrame(rows).to_csv(a.out/'design_support.csv',index=False)
pred=pd.read_csv(a.results/'prediction_summary.csv'); cls=pd.read_csv(a.results/'classification_summary.csv');collision=json.loads((a.out/'collision_summary.json').read_text())
comparison=[]
for scope,alias in [('all','all'),('common_angles_ge_minus4','common_angles_ge_minus4')]:
 ss=pred[(pred.protocol=='LOGO')&(pred.support==alias)].set_index('model');b=next(s for s in collision['scopes'] if s['scope']==scope);base=b['LOGO_train_only_exact_key_mean_RMSE_equal_geometry']
 for model in ['tsk','extra_trees']:
  rmse=float(ss.loc[model,'rmse_dB']);comparison.append(dict(scope=scope,model=model,rmse_dB=rmse,train_only_exact_key_mean_rmse_dB=base,improvement_dB=base-rmse,improvement_relative=(base-rmse)/base))
pd.DataFrame(comparison).to_csv(a.out/'baseline_comparison.csv',index=False)
assert cls.train_unresolved.sum()==0 and cls.joint_unresolved.sum()==0
print('PASS: exact design containment, comparisons and aggregate class checks')
