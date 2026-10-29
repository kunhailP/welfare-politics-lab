"""Construct one matched finite-cohort design for humans and every model arm."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .paired_evaluation import evaluate_arrays
from .contrast_validity import contrast_bounds
from .study1_interest_audit import LEVELS


def matrix_and_contrast(d):
    """Canonical coding, also available for preflight of rank-deficient pilots."""
    arrays, names = [np.ones(len(d))], [('intercept', 'intercept')]
    for feature, levels in LEVELS.items():
        if not set(d[feature]) <= set(levels):
            raise ValueError(f'Unexpected factor level: {feature}')
        for level in levels[1:]:
            arrays.append(d[feature].eq(level).to_numpy(float))
            names.append((feature, level))
    base = np.column_stack(arrays)
    group = d.respondent_income.eq('Low income').to_numpy(float)
    x = np.column_stack([base, base*group[:, None]])
    c = np.zeros(x.shape[1])
    c[names.index(('vignette_income', '$30,000')) + base.shape[1]] = 1
    return x, c


def estimability_diagnostic(x, contrast):
    """Distinguish full coefficient identification from one estimable contrast."""
    x, c = np.asarray(x, float), np.asarray(contrast, float)
    if x.ndim != 2 or c.shape != (x.shape[1],) or not np.isfinite(x).all() or not np.isfinite(c).all():
        raise ValueError('Finite conformable matrix and contrast required')
    _, _, vt = np.linalg.svd(x, full_matrices=False)
    rank = int(np.linalg.matrix_rank(x))
    residual = float(np.linalg.norm(c-vt[:rank].T@(vt[:rank]@c)))
    tolerance = 1e-10*max(1., float(np.linalg.norm(c)))
    return {'rows': len(x), 'columns': x.shape[1], 'rank': rank,
            'all_coefficients_identified_full_rank': rank == x.shape[1],
            'contrast_rowspace_residual_l2': residual, 'contrast_estimability_tolerance': tolerance,
            'contrast_estimable_in_design': residual <= tolerance}


def construct(data, candidate_ids):
    ids = list(candidate_ids)
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate cohort IDs')
    selected = data[data.id.isin(ids)].copy()
    if set(selected.id) != set(ids):
        raise ValueError('Requested cohort member absent from source')
    if selected.duplicated(['id', 'vignette_num']).any():
        raise ValueError('Duplicate source row ID')
    if not selected.groupby('id').size().eq(4).all():
        raise ValueError('Every candidate must retain four profiles')
    if selected[list(LEVELS)].isna().any().any():
        raise ValueError('Primary cohort cannot silently drop incomplete profile rows')
    if selected.vignette_allocation.isna().any() or not selected.vignette_allocation.between(0, 4000).all():
        raise ValueError('Fully observed bounded human reference required')
    for column in ['respondent_income', 'respondent_employment', 'respondent_children']:
        if selected.groupby('id')[column].nunique(dropna=False).gt(1).any():
            raise ValueError('Respondent trait changes inside a source trajectory')
    d = selected[selected.respondent_income.isin(['High income', 'Low income'])].sort_values(['id', 'vignette_num'])
    x, c = matrix_and_contrast(d)
    if np.linalg.matrix_rank(x) != x.shape[1]:
        raise ValueError('Primary design is rank deficient')
    y = d.vignette_allocation.to_numpy(float)
    row_ids = [f's1:{i}:{j}' for i, j in zip(d.id, d.vignette_num)]
    weights = contrast_bounds(x, y, c)['contrast_weights']
    patterns = {group: set(map(tuple, part[list(LEVELS)].to_numpy()))
                for group, part in d.groupby('respondent_income')}
    shared = patterns['High income'] & patterns['Low income']
    metadata = {'estimand': 'finite selected high/low cohort fixed-design contrast',
                'human_uncertainty': 'recorded reference is known; no sampling confidence interval attached',
                'candidate_people': len(ids), 'primary_people': int(d.id.nunique()),
                'primary_rows': len(d), 'design_columns': x.shape[1], 'rank': int(np.linalg.matrix_rank(x)),
                'respondent_groups': d.drop_duplicates('id').respondent_income.value_counts().to_dict(),
                'design_condition_number': float(np.linalg.cond(x)),
                'cohort_sha256': hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest(),
                'design_sha256': hashlib.sha256(np.asarray(x, dtype='<f8').tobytes()).hexdigest(),
                'contrast_sha256': hashlib.sha256(np.asarray(c, dtype='<f8').tobytes()).hexdigest(),
                'row_ids_sha256': hashlib.sha256(json.dumps(row_ids, separators=(',', ':')).encode()).hexdigest(),
                'human_outcomes_sha256': hashlib.sha256(np.asarray(y, dtype='<f8').tobytes()).hexdigest(),
                'contrast_leverage': {'absolute_weight_sum': float(np.abs(weights).sum()),
                                      'largest_absolute_row_weight': float(np.abs(weights).max()),
                                      'by_respondent_income': {group: float(np.abs(weights[d.respondent_income.eq(group)]).sum())
                                                               for group in ['High income', 'Low income']}},
                'full_profile_support': {'distinct_patterns_by_group': {group: len(values) for group, values in patterns.items()},
                                         'shared_exact_eight_factor_patterns': len(shared),
                                         'interpretation': 'Support diagnostic only; additive projection does not require exact matches or imply causal identification.'},
                'joint_income_employment_support': d.groupby(['respondent_income', 'vignette_income', 'vignette_employment'], observed=True).size().rename('rows').reset_index().to_dict('records'),
                'factor_references': {key: value[0] for key, value in LEVELS.items()},
                'point_is_not_a_causal_human_income_effect': True}
    return x, y, c, row_ids, metadata


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path('data/raw'))
    p.add_argument('--cohort', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    cohort = pd.read_csv(args.cohort, sep='\t')
    ids = cohort.loc[(cohort.study == 'study1') & (cohort.phase == 'confirmatory'), 'source_id'].tolist()
    d = pd.read_csv(args.source / 'study1.tab', sep='\t')
    x, y, c, rows, metadata = construct(d, ids)
    np.savez(args.output / 'human_reference_design.npz', x=x, y=y, contrast=c, row_ids=np.asarray(rows))
    (args.output / 'design.json').write_text(json.dumps(metadata, indent=2))
    # This is a software integrity check, never empirical model evidence.
    diagnostic = evaluate_arrays(x, y, {'N': y.copy(), 'F': y.copy(), 'F-I': y.copy()}, c, rows)
    diagnostic['status'] = 'copied_human_reference_software_check_only'
    diagnostic['actual_model_calls'] = 0
    for arm in diagnostic['arms'].values():
        np.testing.assert_allclose(arm['signed_error_bounds'], [0, 0], atol=1e-8)
    (args.output / 'copied_reference_diagnostic.json').write_text(json.dumps(diagnostic, indent=2))
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
