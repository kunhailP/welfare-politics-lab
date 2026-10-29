"""Source-design diagnostics, not a certification of randomized assignment."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .study1_interest_audit import LEVELS


def independence_stat(table):
    table = np.asarray(table, dtype=float)
    expected = table.sum(1)[:, None] * table.sum(0)[None, :] / table.sum()
    active = expected > 0
    return float(np.sum((table[active] - expected[active]) ** 2 / expected[active]))


def blocked_diagnostic(data, group_column, profile_column, replicates=499, seed=20261029):
    ids = np.array(sorted(data.id.unique()))
    people = data.drop_duplicates('id').set_index('id').reindex(ids)
    group, groups = pd.factorize(people[group_column].fillna('NOT_REPORTED'))
    counts = pd.crosstab(data.id, data[profile_column].fillna('NOT_RECORDED')).reindex(ids, fill_value=0)
    blocks = counts.to_numpy(dtype=float)
    def table(labels):
        out = np.zeros((len(groups), blocks.shape[1]))
        np.add.at(out, labels, blocks)
        return out
    observed = table(group)
    stat = independence_stat(observed)
    rng = np.random.default_rng(seed)
    exceed = sum(independence_stat(table(rng.permutation(group))) >= stat for _ in range(replicates))
    return {'respondent_group': group_column, 'recipient_attribute': profile_column,
            'group_levels': list(groups), 'attribute_levels': list(counts.columns),
            'table': observed.astype(int).tolist(), 'descriptive_chi_square': stat,
            'block_permutations': replicates,
            'diagnostic_p_under_respondent_block_exchangeability': (exceed + 1) / (replicates + 1),
            'interpretation': 'Exploratory independence diagnostic preserving four-profile blocks. Not the original randomization test or proof of an assignment failure.'}


def audit(data_dir, replicates=499):
    source = Path(data_dir)
    s1 = pd.read_csv(source / 'study1.tab', sep='\t')
    recipient = list(LEVELS)
    complete = s1[recipient].notna().all(axis=1).groupby(s1.id).all()
    people = s1.drop_duplicates('id').set_index('id')
    people['complete_four_profiles'] = complete
    people['income_group'] = people.respondent_income.fillna('NOT_REPORTED')
    selection = people.groupby('income_group').complete_four_profiles.agg(['size', 'sum', 'mean'])
    report = {'status': 'human_source_diagnostics_only', 'model_calls': 0,
              'assignment_probabilities_verified': False,
              'uniform_assignment_assumed': False,
              'selection_by_respondent_income': [
                  {'group': str(index), 'released_people': int(row['size']),
                   'complete_people': int(row['sum']), 'complete_fraction': float(row['mean'])}
                  for index, row in selection.iterrows()],
              'source_marginals': {},
              'source_missing_cells': {c: int(s1[c].isna().sum()) for c in s1 if s1[c].isna().any()},
              'blocked_association_diagnostics': [blocked_diagnostic(s1, 'respondent_income',
                  c, replicates=replicates) for c in ['vignette_employment', 'vignette_citizen']],
              'consequence': 'Primary human-model benchmark is a fixed-design contrast in complete-profile retained respondents. Do not infer a representative national effect or assume released factor frequencies prove uniform assignment. The observed imbalance does not itself establish that the original experiment was invalid.'}
    for name in ['study1.tab', 'study2.tab', 'study2_alt.tab']:
        d = pd.read_csv(source / name, sep='\t')
        report['source_marginals'][name] = {c: d[c].fillna('NOT_RECORDED').value_counts().to_dict() for c in recipient}
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path('data/raw'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--permutations', type=int, default=499)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    report = audit(args.source, args.permutations)
    (args.output / 'audit.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({'status': report['status'], 'selection': report['selection_by_respondent_income'],
                      'assignment_probabilities_verified': False}, indent=2))


if __name__ == '__main__':
    main()
