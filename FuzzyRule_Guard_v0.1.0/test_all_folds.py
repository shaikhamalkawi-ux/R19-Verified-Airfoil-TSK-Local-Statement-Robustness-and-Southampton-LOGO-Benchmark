from pathlib import Path
import concurrent.futures, json, csv, io, zipfile, sys, hashlib
from collections import Counter
import numpy as np
from fuzzyrule_guard import Model, audit, model_indices, AF4_SHA256

def work(arg):
    path,fold=arg
    with zipfile.ZipFile(path) as arc:
        with np.load(io.BytesIO(arc.read(f'direct_derivative/inputs/states/AIRFOIL_ONESE_fold{fold:02d}.npz')),allow_pickle=False) as z:
            m=Model(z);out=[]
            for j in model_indices(z,None,None):
                r=audit(m,j,.1,.01,.001)
                r['fold']=fold
                for k in ('dual_mu','alternative_beta','delta'):r.pop(k,None)
                out.append(r)
            return out
if __name__=='__main__':
    path=sys.argv[1];out=Path(sys.argv[2]);out.mkdir(exist_ok=True,parents=True)
    with open(path,'rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==AF4_SHA256
    with zipfile.ZipFile(path) as arc:
        expected={(int(r['fold']),int(r['j'])):{'SIGN_PROTECTED_POINTWISE':'PROTECTED','FEASIBLE_REVERSAL':'REVERSIBLE'}[r['final_class']] for r in csv.DictReader(io.StringIO(arc.read('direct_derivative/inputs/RESOLVED_510_STATEMENTS.csv').decode())) if float(r['epsilon'])==.1 and float(r['gamma'])==.001}
    rows=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        for result in pool.map(work,[(path,f) for f in range(10)]):
            rows+=result
            print('fold',result[0]['fold'],dict(Counter(r['status'] for r in result)),flush=True)
    for r in rows:r['expected']=expected[(r['fold'],r['index'])];r['match']=r['expected']==r['status']
    summary={'mode':'fresh solver audit, existing frozen models; not new model fitting','total':len(rows),'matched':sum(r['match'] for r in rows),'counts':dict(Counter(r['status'] for r in rows)),'input_sha256':AF4_SHA256,'max_training_change':max(r['max_training_change'] for r in rows if r['status']=='REVERSIBLE'),'max_objective_increase':max(r['relative_objective_increase'] for r in rows if r['status']=='REVERSIBLE')}
    (out/'fresh_solver_regression.json').write_text(json.dumps({'summary':summary,'rows':rows},indent=2,allow_nan=False)+'\n');print(json.dumps(summary,indent=2),flush=True)
    assert len(rows)==510 and summary['matched']==510
