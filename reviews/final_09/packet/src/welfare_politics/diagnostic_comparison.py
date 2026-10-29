"""Same-output empirical-distribution checks on the fixed primary rows.

All distances are finite descriptive CAD quantities. Missing actions stay in
their original cells/denominators. Bounds use a triangle inequality, not imputed
observations, sampling uncertainty or sharp partial-identification claims.
"""
import numpy as np

from .contrast_validity import absolute_error_range


def layout(x):
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or len(x) == 0 or x.shape[1] < 4 or x.shape[1] % 2 or not np.isfinite(x).all():
        raise ValueError('Expected a finite canonical primary matrix')
    p = x.shape[1] // 2
    base, group = x[:, :p], x[:, p]
    if not np.equal(base[:, 0], 1).all() or not np.isin(group, [0, 1]).all() or not np.array_equal(x[:, p:], base*group[:, None]):
        raise ValueError('Expected recipient basis followed by its group interactions')
    return base, group.astype(int)


def w1_completion_bounds(reference, actions):
    reference, actions = np.asarray(reference, float), np.asarray(actions, float)
    if reference.ndim != 1 or len(reference) == 0 or actions.shape != reference.shape:
        raise ValueError('Equal nonempty fixed row counts required')
    known = ~np.isnan(actions)
    if not np.isfinite(reference).all() or not ((reference >= 0) & (reference <= 4000)).all():
        raise ValueError('Fully observed bounded human reference required')
    if not np.isfinite(actions[known]).all() or not ((actions[known] >= 0) & (actions[known] <= 4000)).all():
        raise ValueError('Invalid model actions must be explicitly missing')
    # Computational anchor only: no missing action becomes an observed 2000.
    anchor = np.where(known, actions, 2000.)
    center = float(np.mean(np.abs(np.sort(reference)-np.sort(anchor))))
    radius = float(2000*np.count_nonzero(~known)/len(actions))
    return {'lower': max(0., center-radius), 'upper': min(4000., center+radius),
            'invalid_rows': int(np.count_nonzero(~known)),
            'sharp_bounds_certified': bool(known.all()),
            'method': 'exact equal-weight W1 if complete; conservative midpoint-anchor triangle bounds otherwise'}


def _partition_distance(reference, actions, labels):
    cells = {}
    for i, key in enumerate(labels):
        cells.setdefault(key, []).append(i)
    lower = upper = mean_lower = mean_upper = 0.
    for indices in cells.values():
        bound = w1_completion_bounds(reference[indices], actions[indices])
        weight = len(indices)/len(reference)
        lower += weight*bound['lower']; upper += weight*bound['upper']
        values = actions[indices]
        known = ~np.isnan(values)
        mean_low = float(np.sum(values[known])/len(indices))
        mean_high = mean_low + 4000*np.count_nonzero(~known)/len(indices)
        error_low, error_high = absolute_error_range((mean_low, mean_high), float(reference[indices].mean()))
        mean_lower += weight*error_low; mean_upper += weight*error_high
    singleton_rows = sum(len(indices) == 1 for indices in cells.values())
    sizes = [len(indices) for indices in cells.values()]
    return {'lower': lower, 'upper': upper, 'cells': len(cells),
            'singleton_cells': singleton_rows, 'singleton_rows': singleton_rows,
            'singleton_row_fraction': singleton_rows/len(reference),
            'cell_size_histogram': {str(size): sizes.count(size) for size in sorted(set(sizes))},
            'weighted_cell_mean_absolute_error_bounds_cad': [mean_lower, mean_upper],
            'weighting': 'fixed cell row count / total fixed rows',
            'exact_if_all_actions_observed': True}


def compare(x, human, actions):
    base, group = layout(x)
    human, actions = np.asarray(human, float), np.asarray(actions, float)
    if human.shape != (len(base),) or actions.shape != human.shape:
        raise ValueError('Outcomes must match the fixed design rows')
    overall = w1_completion_bounds(human, actions)
    profiles = [tuple(row) for row in base]
    joint = [(int(g), profile) for g, profile in zip(group, profiles)]
    report = {'target': 'finite same-row diagnostic comparison; not population inference',
              'full_row_count': len(human), 'invalid_rows': overall['invalid_rows'],
              'global_allocation_w1_cad': overall,
              'respondent_group_weighted_w1_cad': _partition_distance(human, actions, list(group)),
              'pooled_complete_profile_weighted_w1_cad': _partition_distance(human, actions, profiles),
              'group_by_profile_weighted_w1_cad': _partition_distance(human, actions, joint),
              'pass_or_equivalence_threshold_applied': False,
              'exact_reproduction_of_an_external_benchmark': False}
    additive = np.column_stack([base, group])
    if overall['invalid_rows']:
        report['additive_projection'] = {'status': 'not_computed_with_invalid_actions',
                                        'reason': 'No complete-case or imputed full-cohort R2 claim'}
    else:
        human_beta = np.linalg.lstsq(additive, human, rcond=None)[0]
        action_beta = np.linalg.lstsq(additive, actions, rcond=None)[0]
        def r2(values, beta):
            # Even an exactly constant decimal array can have nonzero TSS
            # from rounding its mean. R2 is undefined for that array.
            if np.equal(values, values[0]).all():
                return None
            total = float(np.sum((values-values.mean())**2))
            return None if total == 0 else float(1-np.sum((values-additive@beta)**2)/total)
        full_rank = bool(np.linalg.matrix_rank(additive) == additive.shape[1])
        report['additive_projection'] = {
            'status': 'complete_fixed_rows', 'columns': additive.shape[1], 'full_column_rank': full_rank,
            'human_r2': r2(human, human_beta), 'actions_r2': r2(actions, action_beta),
            'max_absolute_coefficient_difference': float(np.max(np.abs(action_beta-human_beta))) if full_rank else None,
            'fitted_value_difference_rmse': float(np.sqrt(np.mean((additive@action_beta-additive@human_beta)**2))),
            'r2_not_a_coefficient_direction_or_interaction_fidelity_test': True}
    return report
