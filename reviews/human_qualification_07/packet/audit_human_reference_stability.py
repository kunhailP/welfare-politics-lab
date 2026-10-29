"""Exploratory source-cohort sensitivity; no generation or population inference.

The locked main cohort is unchanged. Repeated overlapping draws from the
remaining archive are a sensitivity distribution, not independent replications,
a bootstrap confidence interval, or an external validation dataset.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from welfare_politics.primary_design import matrix_and_contrast
from welfare_politics.study1_interest_audit import LEVELS


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(data):
    d = data.sort_values(['id', 'vignette_num'])
    x, c = matrix_and_contrast(d)
    y = d.vignette_allocation.to_numpy(float)
    b, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1]:
        raise ValueError('Full-rank sensitivity design required')
    high = np.zeros_like(c)
    high[:len(c)//2] = c[len(c)//2:]
    return {
        'people': int(d.id.nunique()), 'rows': len(d), 'rank': int(rank),
        'groups': d.drop_duplicates('id').respondent_income.value_counts().to_dict(),
        'high_group_recipient_30k_minus_120k_cad': float(high @ b),
        'low_group_recipient_30k_minus_120k_cad': float((high+c) @ b),
        'low_minus_high_moderation_cad': float(c @ b),
        'cohort_sha256': hashlib.sha256(json.dumps(sorted(d.id.unique().tolist())).encode()).hexdigest(),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=Path('data/raw/study1.tab'))
    p.add_argument('--cohort', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seed', type=int, default=20261031)
    p.add_argument('--draws', type=int, default=500)
    args = p.parse_args()
    if args.draws < 1:
        raise ValueError('At least one draw required')
    data = pd.read_csv(args.source, sep='\t')
    if data.duplicated(['id', 'vignette_num']).any():
        raise ValueError('Duplicate source row')
    for column in ['respondent_income', 'respondent_employment', 'respondent_children']:
        if data.groupby('id')[column].nunique(dropna=False).gt(1).any():
            raise ValueError('Within-person trait inconsistency')
    observed = (data[list(LEVELS)].notna().all(axis=1)
                & data.vignette_allocation.notna()
                & data.vignette_allocation.between(0, 4000))
    complete = observed.groupby(data.id).all() & data.groupby('id').size().eq(4)
    pool = data[data.id.isin(complete[complete].index)
                & data.respondent_income.isin(['High income', 'Low income'])]
    linkage = pd.read_csv(args.cohort, sep='\t')
    linkage = linkage[linkage.study.eq('study1')]
    if linkage.source_id.duplicated().any():
        raise ValueError('Duplicate candidate person')
    main_ids = set(linkage.loc[linkage.phase.eq('confirmatory'), 'source_id'])
    pilot_ids = set(linkage.loc[linkage.phase.eq('pilot'), 'source_id'])
    if main_ids & pilot_ids or not main_ids or not pilot_ids:
        raise ValueError('Require disjoint existing main and pilot cohorts')
    if not main_ids.union(pilot_ids) <= set(complete[complete].index):
        raise ValueError('Existing candidate cohort is not complete')
    main_data = pool[pool.id.isin(main_ids)]
    remainder = pool[~pool.id.isin(main_ids | pilot_ids)]
    main_summary = summarize(main_data)
    groups = {g: sorted(part.id.unique().tolist())
              for g, part in remainder.groupby('respondent_income')}
    for group, count in main_summary['groups'].items():
        if len(groups.get(group, [])) < count:
            raise ValueError('Insufficient disjoint people to match main composition')
    args.output.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(args.seed)
    draws = []
    with (args.output / 'draw_membership.jsonl').open('w') as f:
        for draw in range(args.draws):
            ids = sorted(int(i) for g in sorted(main_summary['groups'])
                         for i in rng.choice(groups[g], main_summary['groups'][g], replace=False))
            if len(ids) != len(set(ids)) or set(ids) & (main_ids | pilot_ids):
                raise AssertionError('Sensitivity cohort overlap or duplicated person')
            result = summarize(remainder[remainder.id.isin(ids)])
            if result['groups'] != main_summary['groups']:
                raise AssertionError('Composition mismatch')
            draws.append({'draw': draw, **result})
            f.write(json.dumps({'draw': draw, 'source_ids': ids})+'\n')
    fields = ['high_group_recipient_30k_minus_120k_cad',
              'low_group_recipient_30k_minus_120k_cad', 'low_minus_high_moderation_cad']
    distributions = {}
    for field in fields:
        values = np.array([d[field] for d in draws])
        distributions[field] = {
            'quantiles': dict(zip(['min', 'q05', 'q25', 'median', 'q75', 'q95', 'max'],
                                  np.quantile(values, [0, .05, .25, .5, .75, .95, 1]).tolist())),
            'positive_draws': int((values > 0).sum()),
            'negative_draws': int((values < 0).sum()),
            'zero_draws': int((values == 0).sum()),
        }
    (args.output / 'draw_estimates.json').write_text(json.dumps(draws, indent=2))
    report = {
        'status': 'exploratory_human_source_cohort_sensitivity_only',
        'actual_model_calls': 0, 'locked_primary_changed': False,
        'source_sha256': sha256(args.source), 'cohort_linkage_sha256': sha256(args.cohort),
        'script_sha256': sha256(Path(__file__)),
        'seed': args.seed, 'draws': args.draws,
        'main': main_summary, 'disjoint_remainder': summarize(remainder),
        'complete_high_low_pool': summarize(pool),
        'excluded_pilot_high_low_people': int(pool[pool.id.isin(pilot_ids)].id.nunique()),
        'matched_draw_distributions': distributions,
        'limitations': [
            'Human outcomes were already available and inspected; not an untouched holdout.',
            'All cohorts share one source survey and its selection/reconstruction limitations.',
            'Draws overlap with each other but never with the main or pilot people.',
            'Quantiles and sign counts describe these draws; no population CI, p-value, or sign probability.',
            'Different cohorts have different recipient tasks; this varies both people and task composition.',
            'Group differences are descriptive, not causal income or psychological mechanism effects.',
            'No endpoint, cohort or seed was selected to maximize a desired human or model result.',
        ],
    }
    report['artifact_sha256'] = {name: sha256(args.output / name)
                                 for name in ['draw_estimates.json', 'draw_membership.jsonl']}
    (args.output / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
