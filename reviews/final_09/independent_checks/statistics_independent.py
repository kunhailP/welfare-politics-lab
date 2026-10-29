import hashlib,json
from pathlib import Path
import numpy as np,pandas as pd
root=Path('/tmp/welfare_final_blind_09'); out=root/'reviewer_B_scratch'
manifest=json.loads((root/'packet_manifest.json').read_text()); integrity={}
for directory,key in [('packet','packet_files'),('private','private_source_supplement_files')]:
 for name,h in manifest[key].items(): integrity[directory+'/'+name]=hashlib.sha256((root/directory/name).read_bytes()).hexdigest()==h
D=pd.read_csv(root/'private/study1.tab',sep='\t'); L=pd.read_csv(root/'private/cohort_linkage.tsv',sep='\t'); L=L[L.study=='study1']
# Independently transcribed category basis, without importing packet functions.
levels=[('vignette_gender',['Female','Male']),('vignette_citizen',['Not a citizen','Citizen born in Canada','Citizen not born in Canada']),('vignette_health',['Healthy','Poor health']),('vignette_marital',['Single','Married']),('vignette_children',['No children','Children under 5','5-12','Over 12']),('vignette_employment',['Employed full-time','Employed, reduced income','Unemployed due to pandemic','Unemployed']),('vignette_income',['$120,000','$90,000','$60,000','$30,000']),('vignette_ethnicity',['White','East Asian','Indigenous','South Asian'])]
cols=[c for c,_ in levels]; label='vignette_allocation'; group='respondent_income'
valid=D[cols].notna().all(axis=1)&D[label].notna()&D[label].between(0,4000)
comp=valid.groupby(D.id).all()&D.groupby('id').size().eq(4)
complete=D[D.id.isin(comp[comp].index)]; pool=complete[complete[group].isin(['High income','Low income'])]
mainids=set(L.loc[L.phase=='confirmatory','source_id']); pilotids=set(L.loc[L.phase=='pilot','source_id'])
main=pool[pool.id.isin(mainids)].sort_values(['id','vignette_num']); train=pool[~pool.id.isin(mainids|pilotids)].sort_values(['id','vignette_num'])
def base(d):return np.column_stack([np.ones(len(d))]+[d[c].eq(v).to_numpy(float) for c,vs in levels for v in vs[1:]])
def contrast(d,y=None):
 y=d[label].to_numpy() if y is None else np.asarray(y); B=base(d); slopes={}; k=1+sum(len(vs)-1 for c,vs in levels[:6])+2
 for g in ['High income','Low income']:
  ix=d[group].eq(g).to_numpy(); b=np.linalg.solve(B[ix].T@B[ix],B[ix].T@y[ix]); slopes[g]=float(b[k])
 return {'high':slopes['High income'],'low':slopes['Low income'],'gamma':slopes['Low income']-slopes['High income']}
def predict(tr,te,name):
 if name=='B_mean': a=np.ones((len(tr),1)); b=np.ones((len(te),1))
 elif name=='B_recipient_OLS': a=base(tr); b=base(te)
 else:
  # A different parametrization: two disjoint group-specific blocks.
  a0=base(tr);b0=base(te);g0=tr[group].eq('Low income').to_numpy()[:,None];g1=te[group].eq('Low income').to_numpy()[:,None]
  a=np.column_stack([a0*(~g0),a0*g0]);b=np.column_stack([b0*(~g1),b0*g1])
 beta=np.linalg.solve(a.T@a,a.T@tr[label].to_numpy()); raw=b@beta
 return np.clip(raw,0,4000),{'min':float(raw.min()),'max':float(raw.max()),'clipped':int(((raw<0)|(raw>4000)).sum()),'rank':int(np.linalg.matrix_rank(a))}
def err(y,p): return {'rmse':float(np.sqrt(np.mean((y-p)**2))),'mae':float(np.mean(abs(y-p)))}
names=['B_mean','B_recipient_OLS','B_income_interacted_OLS']; rng=np.random.default_rng(20261030)
parts=[np.array_split(rng.permutation(sorted(tr.id.unique())),5) for g,tr in train.groupby(group)]
folds=[set(np.concatenate([x[k] for x in parts])) for k in range(5)]
cv={};models={};saved=np.load(out/'author_reference/statistical_predictions.npz')
for name in names:
 p=np.empty(len(train))
 for ids in folds:
  mask=train.id.isin(ids).to_numpy();p[mask],_=predict(train.loc[~mask],train.loc[mask],name)
 cv[name]=err(train[label].to_numpy(),p)
 p,meta=predict(train,main,name);models[name]={'main':err(main[label].to_numpy(),p),'contrasts':contrast(main,p),'fit':meta,'max_abs_diff_author_prediction':float(abs(saved[name]-p).max())}
people=D.drop_duplicates('id'); rates={}
for g,part in people.groupby(group,dropna=False):rates[str(g)]={'released':len(part),'complete':int(comp.reindex(part.id).sum()),'complete_fraction':float(comp.reindex(part.id).mean())}
result={'manifest_all_match':all(integrity.values()),'manifest_files':len(integrity),'source':{'people':D.id.nunique(),'rows':len(D),'duplicate_keys':int(D.duplicated(['id','vignette_num']).sum()),'complete_people':complete.id.nunique(),'complete_rows':len(complete),'pool_people':pool.id.nunique(),'pool_rows':len(pool),'main_candidate_people':len(mainids),'pilot_candidate_people':len(pilotids),'candidate_overlap':len(mainids&pilotids),'pilot_highlow':pool[pool.id.isin(pilotids)].id.nunique(),'training_people':train.id.nunique(),'training_rows':len(train),'main_people':main.id.nunique(),'main_rows':len(main),'training_main_overlap':len(set(train.id)&set(main.id)),'income_completion':rates,'respondent_missing_rows':D[[c for c in D if c.startswith('respondent_')]].isna().sum().to_dict(),'margins':{c:D[c].value_counts(dropna=False).to_dict() for c in ['vignette_citizen','vignette_employment']}},'contrasts':{n:contrast(d) for n,d in [('main',main),('train',train),('pool',pool)]},'cv':cv,'models':models,'fold_people':[len(f) for f in folds]}
# Independent remaining-source sensitivity draws, using group-wise OLS.
rng=np.random.default_rng(20261031);counts=main.drop_duplicates('id')[group].value_counts().to_dict();groups={g:sorted(part.id.unique()) for g,part in train.groupby(group)};draws=[]
for k in range(500):
 ids=set(int(i) for g in sorted(counts) for i in rng.choice(groups[g],counts[g],replace=False));draws.append(contrast(train[train.id.isin(ids)]))
result['sensitivity']={key:{'quantiles':np.quantile([d[key] for d in draws],[0,.05,.25,.5,.75,.95,1]).tolist(),'negative':sum(d[key]<-1e-8 for d in draws),'positive':sum(d[key]>1e-8 for d in draws)} for key in ['high','low','gamma']}
(out/'independent_results.json').write_text(json.dumps(result,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else float(x)))
print(json.dumps(result,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else float(x)))
