"""Fixed-design OLS contrast bounds for invalid/missing bounded actions.

This is an evaluation utility, not a model-output generator. Bounds cover every
completion of invalid rows by allowed actions. They do not assume random failure
or turn a refusal into an observed allocation. X must be fixed and full rank.
"""
import numpy as np


def contrast_bounds(x, observed, contrast, lower=0.0, upper=4000.0,
                    identification_tolerance=1e-8, maximum_condition=1e10):
    x = np.asarray(x, dtype=float)
    y = np.asarray(observed, dtype=float)
    c = np.asarray(contrast, dtype=float)
    if x.ndim != 2 or min(x.shape) == 0 or y.shape != (x.shape[0],) or c.shape != (x.shape[1],):
        raise ValueError('Shape mismatch')
    if not np.isfinite(x).all() or not np.isfinite(c).all() or not np.isfinite([lower, upper]).all() or not lower < upper:
        raise ValueError('Invalid fixed design or action bounds')
    u, singular, vt = np.linalg.svd(x, full_matrices=False)
    rank_tolerance = np.finfo(float).eps * max(x.shape) * singular[0]
    if len(singular) != x.shape[1] or singular[-1] <= rank_tolerance:
        raise ValueError('Contrast design must have full column rank')
    condition = float(singular[0] / singular[-1])
    if condition > maximum_condition:
        raise ValueError('Design is too ill-conditioned for this numerical implementation')
    known = ~np.isnan(y)
    if not np.isfinite(y[known]).all() or ((y[known] < lower) | (y[known] > upper)).any():
        raise ValueError('Mark invalid outputs as missing before computing completion bounds')
    # Minimum-norm solution to X' w = c; avoid squaring conditioning through X'X.
    weights = u @ ((vt @ c) / singular)
    fixed = float(weights[known] @ y[known])
    unknown = weights[~known]
    low = fixed + np.minimum(unknown * lower, unknown * upper).sum()
    high = fixed + np.maximum(unknown * lower, unknown * upper).sum()
    width = float(high - low)
    return {'lower': float(low), 'upper': float(high), 'invalid_rows': int((~known).sum()),
            'completion_width': width, 'missing_weight_l1': float(np.abs(unknown).sum()),
            'design_condition_number': condition,
            'point_identified_in_fixed_design': bool(width <= identification_tolerance),
            'identification_tolerance_cad': identification_tolerance,
            'contrast_weights': weights}


def absolute_error_range(interval, reference):
    """Conservative range over the interval hull, including integer actions."""
    low, high = interval
    if low > high or not np.isfinite([low, high, reference]).all():
        raise ValueError('Invalid contrast interval or reference')
    smallest = 0.0 if low <= reference <= high else min(abs(low-reference), abs(high-reference))
    return (float(smallest), float(max(abs(low-reference), abs(high-reference))))


def error_change_bounds(first_interval, baseline_interval, reference):
    """Range for |first-reference|-|baseline-reference|; negative means closer.

    Invalid arm completions have no assumed cross-arm restrictions. This is a
    conservative interval-hull range, not a confidence interval or necessarily
    sharp for the discrete integer-action lattice.
    """
    first = absolute_error_range(first_interval, reference)
    base = absolute_error_range(baseline_interval, reference)
    return {'lower': first[0]-base[1], 'upper': first[1]-base[0],
            'interpretation': 'conservative completion bounds; not sampling uncertainty'}


def verify_with_exhaustive_completions():
    """An adversarial failure pattern with a directly enumerable reference."""
    from itertools import product
    rng = np.random.default_rng(20261029)
    group = np.repeat([0., 1.], 12)
    recipient = np.tile(np.repeat([0., 1.], 6), 2)
    x = np.column_stack([np.ones(24), group, recipient, group * recipient])
    full = rng.integers(0, 4001, 24).astype(float)
    missing = [0, 3, 12, 15, 23]
    y = full.copy(); y[missing] = np.nan
    c = np.array([0., 0., 0., 1.])
    result = contrast_bounds(x, y, c)
    values = []
    for endpoints in product([0., 4000.], repeat=len(missing)):
        completion = y.copy(); completion[missing] = endpoints
        beta = np.linalg.lstsq(x, completion, rcond=None)[0]
        values.append(float(c @ beta))
    np.testing.assert_allclose([result['lower'], result['upper']], [min(values), max(values)], atol=1e-8)
    original = float(c @ np.linalg.lstsq(x, full, rcond=None)[0])
    assert result['lower'] <= original <= result['upper']
    exact = contrast_bounds(x, full, c)
    np.testing.assert_allclose([exact['lower'], exact['upper']], [original, original], atol=1e-8)
    return {'status': 'software_validation_only', 'endpoint_completions_enumerated': len(values),
            'missing_records': len(missing), 'bounds': [result['lower'], result['upper']],
            'original_complete_contrast': original, 'model_calls': 0}


if __name__ == '__main__':
    import json
    print(json.dumps(verify_with_exhaustive_completions(), indent=2))
