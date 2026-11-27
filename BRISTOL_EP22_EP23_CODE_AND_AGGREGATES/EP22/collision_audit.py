#!/usr/bin/env python3
"""Post hoc finite-sample geometry-blind information audit. No new model tuning.
Requires rights-cleared local Bristol source ZIP; only aggregate output is written.
Exact observed keys are (geometric angle in deg, frequency in Hz).
"""
import argparse, collections, hashlib, json, math, zipfile, io
from pathlib import Path
import numpy as np
import h5py
import pandas as pd
SHA='a01cc8c447a964e2698755090f55babf447ca370c9edb4a1f1ef88cc4ca2311a'

def main():
 p=argparse.ArgumentParser();p.add_argument('--source-zip',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 assert hashlib.sha256(a.source_zip.read_bytes()).hexdigest()==SHA
 rows=[]
 with zipfile.ZipFile(a.source_zip) as z:
  assert z.testzip() is None
  for name in sorted(n for n in z.namelist() if n.endswith('_ff_sound.h5')):
   geo=Path(name).parent.name
   with h5py.File(io.BytesIO(z.read(name)),'r') as h:
    alpha=h['angles'][:].ravel(); f=h['f'][:]; y=h['spl'][:]
    assert f.shape==y.shape==(len(alpha),12)
    assert np.isfinite(f).all() and np.isfinite(y).all() and np.isfinite(alpha).all() and (f>0).all()
    for i,ang in enumerate(alpha):
     for j,freq in enumerate(f[i]): rows.append((geo,float(ang),float(freq),float(y[i,j])))
 d=pd.DataFrame(rows,columns=['geometry','angle','frequency','y']);keys=['angle','frequency'];assert len(d)==1464 and d.geometry.nunique()==4 and not d.duplicated(['geometry']+keys).any()
 assert len(d[['geometry','angle']].drop_duplicates())==122
 def summarize(d,label):
  geos=sorted(d.geometry.unique()); sizes=d.geometry.value_counts(); d=d.copy(); d['wrow']=1/len(d);d['wgeo']=1/(len(geos)*d.geometry.map(sizes));
  cells=d.groupby(keys);n=cells.size(); assert n.min()>=2
  assert d.groupby(keys).geometry.nunique().equals(n)
  out={'scope':label,'rows':len(d),'spectra':len(d[['geometry','angle']].drop_duplicates()),'distinct_keys':len(n),'multiplicity_histogram':{str(k):int(v) for k,v in n.value_counts().sort_index().items()},'keys_with_disagreeing_y':int((cells.y.max()>cells.y.min()).sum()),'rows_with_cross_geometry_match':int(n[n>1].sum()),'max_response_range_dB':float((cells.y.max()-cells.y.min()).max())}
  for w in ('wrow','wgeo'):
   # Path A: residual-to-weighted-mean sum. Path B: independent pairwise identity.
   loss=0.;pair=0.;normal=0.;
   for _,g in cells:
    yy=g.y.to_numpy();ww=g[w].to_numpy();W=ww.sum();mu=np.dot(ww,yy)/W
    loss+=np.dot(ww,(yy-mu)**2);normal=max(normal,abs(np.dot(ww,yy-mu)))
    for i in range(len(yy)):
     for j in range(i+1,len(yy)):pair+=ww[i]*ww[j]*(yy[i]-yy[j])**2/W
   assert abs(loss-pair)<1e-10 and normal<1e-12
   out[w+'_oracle_MSE']=loss;out[w+'_oracle_RMSE']=math.sqrt(loss);out[w+'_pairwise_MSE']=pair
  fold=[]
  for geo in geos:
   tr=d[d.geometry!=geo];te=d[d.geometry==geo].copy();mu=tr.groupby(keys).y.mean().rename('pred');te=te.join(mu,on=keys,validate='many_to_one');assert te.pred.notna().all()
   err=(te.y-te.pred)**2;fold.append({'scope':label,'heldout_geometry':geo,'test_rows':len(te),'exact_key_matches':int(te.pred.notna().sum()),'mse_dB2':float(err.mean()),'rmse_dB':float(np.sqrt(err.mean()))})
  out['LOGO_train_only_exact_key_mean_RMSE_equal_geometry']=math.sqrt(np.mean([r['mse_dB2'] for r in fold]));out['LOGO_train_only_exact_key_mean_RMSE_equal_row']=math.sqrt(np.average([r['mse_dB2'] for r in fold],weights=[r['test_rows'] for r in fold]));
  return out,fold
 all_,f1=summarize(d,'all');common,f2=summarize(d[d.angle>=-4],'common_angles_ge_minus4')
 assert common['distinct_keys']==360 and common['multiplicity_histogram']=={'4':360}
 # On the balanced 4-geometry common grid, every held-out residual is G/(G-1)
 # times its residual to the all-geometry mean. Verify without using that mean for prediction.
 assert abs(common['LOGO_train_only_exact_key_mean_RMSE_equal_geometry']-4/3*common['wgeo_oracle_RMSE'])<1e-12
 out={'status':'PASS','source_sha256':SHA,'scope':'post hoc descriptive finite-sample, no causal or population claim','scopes':[all_,common],'common_grid_LOGO_identity':'RMSE_LOGO_mean = 4/3 * RMSE_pooled_oracle'}
 (a.out/'collision_summary.json').write_text(json.dumps(out,indent=2)+'\n');pd.DataFrame(f1+f2).to_csv(a.out/'fold_mean_baseline.csv',index=False);print(json.dumps(out,indent=2));print(pd.DataFrame(f1+f2).to_string(index=False))
if __name__=='__main__':main()
