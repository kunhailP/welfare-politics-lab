import hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

root = Path('/tmp/welfare_final_blind_09')
d = pd.read_csv(root/'private/study1.tab', sep='\t')
link = pd.read_csv(root/'private/cohort_linkage.tsv', sep='\t')
factors = [c for c in d if c.startswith('vignette_') and c not in ['vignette_num','vignette_allocation']]
complete = d[factors+['vignette_allocation']].notna().all(axis=1)
ids = d.assign(complete=complete).groupby('id').agg(n=('complete','size'), complete=('complete','all'))
complete_ids = set(ids.index[(ids.n==4)&ids.complete])
main_ids = set(link.loc[(link.study=='study1')&(link.phase=='confirmatory'),'source_id'])
pilot_ids = set(link.loc[(link.study=='study1')&(link.phase=='pilot'),'source_id'])

def analyze(selected):
    data = d[d.id.isin(selected)&d.respondent_income.isin(['High income','Low income'])].copy()
    slopes = {}
    ranks = {}
    for group, part in data.groupby('respondent_income'):
        # Build independent separate-group treatment-coded additive regressions.
        cols = [np.ones(len(part))]
        names = ['intercept']
        for f in factors:
            levels = sorted(d[f].dropna().unique())
            if f=='vignette_income': levels=['$120,000']+[v for v in levels if v!='$120,000']
            for level in levels[1:]:
                cols.append((part[f]==level).to_numpy(float)); names.append((f,level))
        x=np.column_stack(cols)
        b=np.linalg.lstsq(x,part.vignette_allocation.to_numpy(float),rcond=None)[0]
        slopes[group]=float(b[names.index(('vignette_income','$30,000'))])
        ranks[group]=int(np.linalg.matrix_rank(x))
    return {'people':int(data.id.nunique()),'rows':len(data),'groups':data.drop_duplicates('id').respondent_income.value_counts().to_dict(),'ranks':ranks,'slopes':slopes,'gamma':slopes['Low income']-slopes['High income']}

people = d.drop_duplicates('id')
report = {'released_people':int(d.id.nunique()),'released_rows':len(d),'complete_four_profile_people':len(complete_ids),
 'complete_fraction_by_income':people.assign(complete=people.id.isin(complete_ids)).groupby('respondent_income').complete.agg(['sum','count','mean']).to_dict('index'),
 'main':analyze(main_ids),'remainder':analyze(complete_ids-main_ids-pilot_ids),'complete_pool':analyze(complete_ids),
 'recipient_margins':{f:d[f].value_counts(dropna=False).to_dict() for f in ['vignette_citizen','vignette_employment']}}
out=root/'scratch_science/independent_summary.json'
out.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
