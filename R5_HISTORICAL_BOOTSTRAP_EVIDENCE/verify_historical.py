#!/usr/bin/env python3
"""Verify stored historical outputs, not a refit. Python 3 + numpy + scipy + pandas."""
from pathlib import Path
import csv, json, hashlib, itertools, warnings
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.special import logsumexp
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

def assign(sim,t):
    R,S=sim.shape
    i,j=linear_sum_assignment(-np.c_[sim-t,np.zeros((R,R))])
    out=np.full(R,-1,int)
    for a,b in zip(i,j):
        if b<S and sim[a,b]>=t:out[a]=b
    return out

def close(v,e,field):
    err=abs(v-e)
    if not np.isclose(v,e,rtol=2e-7,atol=2e-6):raise AssertionError((field,v,e,err))
    maxerr[field]=max(maxerr.get(field,0.),float(err)); return 1

manifest=json.loads((ROOT/'ORIGINAL_SELECTED_MANIFEST.json').read_text())
for n,v in manifest['selected_original_files'].items():
    b=(ROOT/n).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
prov=json.loads((ROOT/'SOURCE_PROVENANCE.json').read_text())
assert sha((ROOT/'external_source_verification_v3.json').read_bytes())==prov['historical_source_record_sha256']
assert sha((ROOT/'data/airfoil_F5_SEMANTICALLY_VERIFIED.csv').read_bytes())==prov['historical_R5_data_sha256']
d=pd.read_csv(ROOT/'data/airfoil_F5_SEMANTICALLY_VERIFIED.csv');assert len(d)==1503 and d.group_id.nunique()==106
assert np.array_equal(d.row_id,np.arange(1,1504))
g=d.group_id.to_numpy(); counts={'attempts':0,'successful':0,'failed':0,'seed_checks':0,'matching_assignment_checks':0,'summary_scalar_checks':0,'summary_rows':0,'branch_files':0,'parent_files':0};maxerr={}; failures=[];coverage=[];summary=[]
for f,k,s in itertools.product(('F4','F5'),range(10),('compact','reference')):
    task=ROOT/'results/bootstrap'/f'{f}_fold{k:02d}_{s}'
    pp=ROOT/'results/tsk'/f'group_log_{f}'/f'fold_{k:02d}'/('TSK-Ridge-oneSE.npz' if s=='compact' else 'TSK-Ridge-fixedR6h1.npz')
    cols=['frequency_Hz','angle_deg','chord_m','velocity_m_s']+(['displacement_m'] if f=='F5' else [])
    X=d[cols].to_numpy(float).copy();X[:,0]=np.log10(X[:,0]);
    if f=='F5':X[:,-1]=np.log10(X[:,-1])
    complete=json.loads((task/'COMPLETE.json').read_text()); assert complete['n_logged_replicates']==700
    sums=pd.read_csv(task/'SUMMARY.csv');assert len(sums)==4
    counts['parent_files']+=1
    with np.load(pp,allow_pickle=False) as p:
        tr,te=p['tr'],p['te'];assert len(tr)+len(te)==len(d) and len(np.unique(np.r_[tr,te]))==len(d) and not set(g[tr])&set(g[te])
        Z=(X[tr]-p['train_scaler_mean'])/p['train_scaler_scale']; W=p['W_train'];Rt=int(p['selected_R']);
        a=-.5*np.sum(((Z[:,None,:]-p['centers'][None,:,:])/p['widths'][None,:,:])**2,axis=2); assert np.allclose(W,np.exp(a-logsumexp(a,axis=1,keepdims=True)),rtol=1e-10,atol=1e-12)
        parent=p['coef'].reshape(Rt,-1).copy();parent[:,0]+=float(p['train_target_mean'])
        anchors=[np.flatnonzero(W[:,r]>=.1) for r in range(Rt)]
        for branch,B in [('fixed',500),('relearn',200)]:
            logs=pd.read_csv(task/f'{branch}_replicate_register.csv'); assert len(logs)==B and np.array_equal(logs.replicate,np.arange(B))
            assert set(logs.status)<= {'success','FAILED'}
            valid=logs.status.eq('success'); ns=int(valid.sum()); nf=B-ns
            assert ns==complete[f'n_success_{branch}']; failures.extend(logs.loc[~valid].to_dict('records'))
            seed=np.array([int.from_bytes(hashlib.sha256(f'20261007|{f}|{k}|{branch}_{s}|{b}'.encode()).digest()[:4],'little') for b in range(B)])
            assert np.array_equal(seed,logs.seed)
            with np.load(task/f'{branch}_replicate_results.npz',allow_pickle=False) as v:
                assert np.array_equal(v['seeds'],seed); assert int(v['parent_R'])==Rt and float(v['parent_h'])==float(p['h']) and float(v['parent_lambda'])==float(p['lambda_'])
                assert np.array_equal(v['parent_support_sizes'],[len(q) for q in anchors]); assert np.allclose(v['parent_coeff'],parent,rtol=1e-12,atol=1e-12)
                match,sim=v['match'],v['sim']; assert match.shape==(ns,Rt) and sim.shape==(ns,Rt,Rt);assert np.isfinite(sim).all() and np.all((sim>=-1e-12)&(sim<=1+1e-12))
                for i,(M,S) in enumerate(zip(match,sim)):
                    assert np.array_equal(M,assign(S,.5));
                    reg=logs.loc[valid].iloc[i]; assert int(reg.n_matched)==np.sum(M>=0)
                    for t,key in ((.3,'n_above_0p3'),(.7,'n_above_0p7')):assert int(reg[key])==np.sum(assign(S,t)>=0)
                counts['matching_assignment_checks']+=ns*3
                for fit in ('LS','Ridge'):
                    P,C=v[f'{fit}_preds'],v[f'{fit}_coeff'];assert P.shape==(ns,len(te)) and C.shape==(ns,Rt,len(cols)+1) and np.isfinite(P).all()
                    assert np.array_equal(np.isfinite(C).all(axis=-1),match>=0)
                    assert np.isnan(C[match<0]).all()
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore',RuntimeWarning); cs=np.nanstd(C,axis=0,ddof=1);cs=cs[np.isfinite(cs)]
                    loc=[]
                    for r,an in enumerate(anchors):
                        cc=C[match[:,r]>=0,r,:]
                        if len(an) and len(cc)>=2:
                            L=cc[:,0,None]+cc[:,1:]@Z[an].T
                            loc.append(np.sqrt(np.mean(np.var(L,axis=0,ddof=1))))
                    ps=np.std(P,axis=0,ddof=1);_,ix=np.unique(g[te],return_inverse=True)
                    calc={'matched_rule_fraction':np.mean(match>=0),'fraction_fully_matched':np.mean(np.all(match>=0,axis=1)),'coef_sd_median':np.median(cs),'coef_sd_p90':np.quantile(cs,.9),'local_disp_rms_median':np.median(loc),'local_disp_rms_p90':np.quantile(loc,.9),'pred_disp_rms':np.sqrt(np.mean(np.bincount(ix,weights=ps**2)/np.bincount(ix))),'point_sd_median':np.median(ps),'point_sd_p90':np.quantile(ps,.9)}
                    row=sums[(sums.branch==branch)&(sums.fit==fit)].iloc[0]; assert (int(row.B_expected),int(row.B_success),int(row.B_failure))==(B,ns,nf)
                    for field,val in calc.items(): counts['summary_scalar_checks']+=close(val,float(row[field]),field)
                    counts['summary_rows']+=1
                    summary.append(row.to_dict())
            counts['attempts']+=B;counts['seed_checks']+=B;counts['successful']+=ns;counts['failed']+=nf;counts['branch_files']+=1
            coverage.append({'feature':f,'fold':k,'structure':s,'branch':branch,'expected':B,'success':ns,'fail':nf})
assert counts['attempts']==28000 and counts['successful']==27998 and counts['failed']==2 and counts['branch_files']==80 and counts['parent_files']==40
cov=pd.DataFrame(coverage);pd.testing.assert_frame_equal(cov,pd.read_csv(ROOT/'results/BOOTSTRAP_REPLICATE_COVERAGE.csv'),check_dtype=False)
fd=pd.DataFrame(failures);fr=pd.read_csv(ROOT/'results/BOOTSTRAP_FAILED_REPLICATES.csv');assert list(fd[['feature','fold','structure','replicate','seed','error']].itertuples(index=False,name=None))==list(fr[['feature','fold','structure','replicate','seed','error']].itertuples(index=False,name=None))
tab=pd.DataFrame(summary); orig=pd.read_csv(ROOT/'results/TABLE_BOOTSTRAP_FOLD_SUMMARY.csv');pd.testing.assert_frame_equal(tab.reset_index(drop=True),orig,check_dtype=False,rtol=1e-12,atol=1e-12)
agg=tab.groupby(['feature','structure','branch','fit']).agg(successful_draws=('B_success','sum'),failed_draws=('B_failure','sum'),median_pred_disp_rms=('pred_disp_rms','median'),median_local_disp_rms=('local_disp_rms_median','median'),median_coefficient_sd=('coef_sd_median','median'),median_rule_match_fraction=('matched_rule_fraction','median')).reset_index()
pd.testing.assert_frame_equal(agg,pd.read_csv(ROOT/'results/TABLE_BOOTSTRAP_SUMMARY.csv'),check_dtype=False,rtol=1e-12,atol=1e-12)
print(json.dumps({'status':'PASS','selected_original_hash_checks':len(manifest['selected_original_files']),**counts,'aggregate_rows':len(agg),'max_absolute_summary_differences':maxerr,'note':'Stored-output verification, not refitting or recovery of missing historical antecedent states.'},indent=2))
