"""Fixed-design OLS contrast bounds for invalid/missing bounded actions.

This is an evaluation utility, not a model-output generator. Bounds cover every
completion of invalid rows by allowed actions. They do not assume random failure
or turn a refusal into an observed allocation. X must be fixed and full rank.
"""
import numpy as np


def contrast_bounds(x, observed, contrast, lower=0.0, upper=4000.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(observed, dtype=float)
    c = np.asarray(contrast, dtype=float)
    if x.ndim != 2 or y.shape != (x.shape[0],) or c.shape != (x.shape[1],):
        raise ValueError('Shape mismatch')
    if not np.isfinite(x).all() or not np.isfinite(c).all() or not np.isfinite([lower, upper]).all() or not lower < upper:
        raise ValueError('Invalid fixed design or action bounds')
    if np.linalg.matrix_rank(x) != x.shape[1]:
        raise ValueError('Contrast design must have full column rank')
    known = ~np.isnan(y)
    if not np.isfinite(y[known]).all() or ((y[known] < lower) | (y[known] > upper)).any():
        raise ValueError('Mark invalid outputs as missing before computing completion bounds')
    weights = x @ np.linalg.solve(x.T @ x, c)
    fixed = float(weights[known] @ y[known])
    unknown = weights[~known]
    low = fixed + np.minimum(unknown * lower, unknown * upper).sum()
    high = fixed + np.maximum(unknown * lower, unknown * upper).sum()
    return {'lower': float(low), 'upper': float(high), 'invalid_rows': int((~known).sum()),
            'point_identified_in_fixed_design': bool(known.all()), 'contrast_weights': weights}


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
