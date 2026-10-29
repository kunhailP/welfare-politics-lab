"""Check fixed resource prefixes, not power or model fidelity; never generate."""
import argparse
import json
from pathlib import Path

import pandas as pd

from welfare_politics.primary_design import construct, estimability_diagnostic, matrix_and_contrast


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path('data/raw'))
    p.add_argument('--cohort', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    data = pd.read_csv(args.source/'study1.tab', sep='\t')
    cohort = pd.read_csv(args.cohort, sep='\t')
    reports = []
    for phase, count in [('pilot', 32), ('confirmatory', 256), ('confirmatory', 512), ('confirmatory', 768)]:
        ids = cohort.loc[(cohort.study == 'study1') & (cohort.phase == phase), 'source_id'].tolist()[:count]
        if len(ids) != count:
            raise ValueError('Requested tier is not present in frozen cohort')
        people = data[data.id.isin(ids)].drop_duplicates('id')
        primary = int(people.respondent_income.isin(['High income', 'Low income']).sum())
        row = {'phase': phase, 'candidate_people': count, 'primary_high_low_people': primary,
               'primary_rows': primary*4, 'primary_pair_requests_per_rollout': primary*6,
               'three_full_rollouts_pair_requests': primary*18,
               'size_does_not_establish_power_or_importance': True}
        selected = data[data.id.isin(ids) & data.respondent_income.isin(['High income', 'Low income'])].sort_values(['id', 'vignette_num'])
        x, contrast = matrix_and_contrast(selected)
        row['estimability'] = estimability_diagnostic(x, contrast)
        try:
            *_, metadata = construct(data, ids)
            row.update(current_full_rank_evaluator_accepts=True, design_columns=metadata['design_columns'],
                       rank=metadata['rank'], condition=metadata['design_condition_number'])
        except ValueError as exc:
            row.update(current_full_rank_evaluator_accepts=False, reason=str(exc))
        reports.append(row)
    report = {'status': 'human_design_only_no_generation', 'actual_model_calls': 0,
              'tiers': reports,
              'interpretation': 'Full-rank evaluator rejection is not proof that the particular contrast is unidentifiable: inspect its row-space residual. Pilot format success does not certify main-score stability. Resource prefixes change the exact finite target.'}
    with args.output.open('x') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
