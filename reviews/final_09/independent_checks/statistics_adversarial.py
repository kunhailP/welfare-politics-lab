import json,copy,itertools,sys
from pathlib import Path
import numpy as np,pandas as pd
from welfare_politics.contrast_validity import contrast_bounds
from welfare_politics.paired_evaluation import group_component_bounds
from welfare_politics.diagnostic_comparison import compare
from welfare_politics.render import parse_pair,ARMS,message_digest,request_identity
from welfare_politics.recorded_responses import assemble,IDENTITY
from welfare_politics.statistical_references import fit_predict,eligible_pool
root=Path('/tmp/welfare_final_blind_09'); out=root/'reviewer_B_scratch';d=pd.read_csv(root/'private/study1.tab',sep='\t');l=pd.read_csv(root/'private/cohort_linkage.tsv',sep='\t');l=l[l.study=='study1'];m=set(l.loc[l.phase=='confirmatory','source_id']);p=set(l.loc[l.phase=='pilot','source_id'])
# Independent source-based design generated from the independent checker namespace.
scope={};exec((out/'independent.py').read_text().split("result={'manifest_all_match'")[0],scope)
main=scope['main'];train=scope['train'];base=scope['base'](main);g=main.respondent_income.eq('Low income').to_numpy(float);x=np.column_stack([base,base*g[:,None]]);y=main.vignette_allocation.to_numpy(float);c=np.zeros(36);c[31]=1
# Canonical recipient-income coefficient position, not a magic assumed value.
c[:]=0;idx=1+sum(len(v)-1 for _,v in scope['levels'][:6])+2;c[18+idx]=1
missing=[0,1,1200,1201,1300,1301];ym=y.copy();ym[missing]=np.nan
bounds=contrast_bounds(x,ym,c);values=[]
for ends in itertools.product([0,4000],repeat=len(missing)):
 full=ym.copy();full[missing]=ends;values.append(c@np.linalg.lstsq(x,full,rcond=None)[0])
comp=group_component_bounds(x,ym,c)
summary={'linear_source_endpoint_completions':len(values),'linear_endpoint_bounds':[min(values),max(values)],'reported_linear_bounds':[bounds['lower'],bounds['upper']],'max_linear_endpoint_error':float(np.max(abs(np.array([min(values),max(values)])-[bounds['lower'],bounds['upper']]))),'component_rectangle_error':float(np.max(abs(np.array([bounds['lower'],bounds['upper']])-[comp['low_income']['lower']-comp['high_income']['upper'],comp['low_income']['upper']-comp['high_income']['lower']])))}
# Fully-missing case must preserve the finite denominator and actual allowed set.
summary['all_missing_mean']=contrast_bounds(np.ones((4,1)),[np.nan]*4,[1])
dist=compare(x,y,y);summary['real_group_profile_cells']=dist['group_by_profile_weighted_w1_cad'];summary['pooled_cells']=dist['pooled_complete_profile_weighted_w1_cad']['cells']
# Source-level leakage perturbation: target labels and IDs cannot affect prediction.
leaks={}
for name in ['B_mean','B_recipient_OLS','B_income_interacted_OLS']:
 first,_=fit_predict(train,main,name);altered=main.copy();altered['vignette_allocation']=-1e12;altered['id']=altered.id+10**8;second,_=fit_predict(train,altered,name);leaks[name]=float(abs(first-second).max())
summary['source_target_label_id_perturbation_max_diff']=leaks
# Recreate cohort draw independent of supplied linkage; S1 draw precedes all S2 operations.
elig=d[[c for c,_ in scope['levels']]].notna().all(axis=1).groupby(d.id).all();order=np.random.default_rng(20261029).permutation(sorted(elig[elig].index));summary['seeded_pilot_linkage_matches']=set(order[:32])==p;summary['seeded_main_linkage_matches']=set(order[32:800])==m
# Parser adversarial classes.
summary['parser']={}
for name,raw in [('bool','{"A":0,"B":true}'),('float','{"A":1.0,"B":2}'),('duplicate','{"A":1,"A":2,"B":3}'),('nan','{"A":NaN,"B":1}'),('fence','```json\n{"A":1,"B":2}\n```'),('nested','['*1100+'0'+']'*1100)]:
 try:summary['parser'][name]=parse_pair(raw)['status']
 except Exception as e:summary['parser'][name]='RAISED '+type(e).__name__
# Minimal complete replay; reversed A/B mapping and shuffled logs have distinct amounts.
rows=[f's1:999:{i}' for i in [1,2,3,4]];requests=[];attempts=[]
for arm in ARMS:
 for nums in [[2,1],[4,3]]:
  r={'agent_id':'s1:999','arm':arm,'profile_numbers':nums,'rollout':0,'messages':[{'role':'user','content':'synthetic probe'}]};r['messages_sha256']=message_digest(r['messages']);r['request_id']=request_identity(r);requests.append(r);attempts.append({**{k:r[k] for k in IDENTITY},'attempt':1,'status':'reply','raw_reply':json.dumps({slot:i*101 for slot,i in zip(['A','B'],nums)}),'returned_model_id':'fixture','cost_usd':0})
a,receipt=assemble(requests,list(reversed(attempts)),rows,'fixture');summary['reversed_keyed_mapping_correct']=all(np.array_equal(v,[101,202,303,404]) for v in a.values())
for name,mutator in [('missing_log',lambda a:a.pop()),('post_reply_retry',lambda a:a.append({**a[0],'attempt':2})),('wrong_model',lambda a:a[0].update(returned_model_id='wrong'))]:
 b=copy.deepcopy(attempts);mutator(b)
 try:assemble(requests,b,rows,'fixture');summary['replay_'+name]='ACCEPTED'
 except ValueError:summary['replay_'+name]='rejected'
# Internal hash consistency is distinct from binding to a trusted frozen request plan.
rq=copy.deepcopy(requests);at=copy.deepcopy(attempts);rq[0]['messages'][0]['content']='new semantic task';rq[0]['messages_sha256']=message_digest(rq[0]['messages']);rq[0]['request_id']=request_identity(rq[0]);at[0].update({k:rq[0][k] for k in IDENTITY})
try:assemble(rq,at,rows,'fixture');summary['self_rehashed_changed_prompt']='accepted_without_external_manifest'
except Exception as e:summary['self_rehashed_changed_prompt']=type(e).__name__
# Compare rerun result to frozen author result, recursively, reporting discrepancies only.
a=json.loads((root/'packet/author_reference_results.json').read_text());b=json.loads((out/'author_reference/report.json').read_text());diff=[]
def walk(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  for k in set(a)|set(b):
   if k not in a or k not in b:diff.append([path+'/'+k,'missing'])
   else:walk(a[k],b[k],path+'/'+k)
 elif isinstance(a,list) and isinstance(b,list):
  if len(a)!=len(b):diff.append([path,'length'])
  else:
   for i,(v,w) in enumerate(zip(a,b)):walk(v,w,path+'/'+str(i))
 elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
  if abs(a-b)>1e-7:diff.append([path,a,b])
 elif a!=b:diff.append([path,a,b])
walk(a,b);summary['author_report_differences_gt_1e7']=diff
# Missing source outcomes and row labels.
summary['source_missing_outcomes']=int(d.vignette_allocation.isna().sum());summary['source_out_of_bounds']=int((~d.vignette_allocation.between(0,4000)&d.vignette_allocation.notna()).sum());summary['source_vignette_numbers']=sorted(d.vignette_num.unique().tolist())
(out/'adversarial_results.json').write_text(json.dumps(summary,indent=2,default=lambda x:x.tolist() if isinstance(x,np.ndarray) else float(x)))
print(json.dumps(summary,indent=2,default=lambda x:x.tolist() if isinstance(x,np.ndarray) else float(x)))
