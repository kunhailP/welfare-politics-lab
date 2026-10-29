"""Descriptive matched-design evaluation of one recorded model rollout.

This module makes no superpopulation or decoding-expectation inference. The
same rows/design are used for human and all arms, including invalid-action rows.
"""
import hashlib
import json

import numpy as np

from .contrast_validity import contrast_bounds, error_change_bounds


def evaluate(x, human, model_arms, contrast, row_ids):
    x = np.asarray(x, dtype=float)
    human = np.asarray(human, dtype=float)
    ids = [value.item() if isinstance(value, np.generic) else value for value in row_ids]
    if len(ids) != len(human) or len(set(ids)) != len(ids):
        raise ValueError('Row identifiers must be unique and aligned with outcomes')
    h = contrast_bounds(x, human, contrast)
    if not h['point_identified_in_fixed_design'] or h['invalid_rows']:
        raise ValueError('Primary human reference must be fully observed on the frozen design')
    gamma_h = h['lower']
    result = {'target': 'finite matched cohort, fixed design, one recorded rollout',
              'sampling_confidence_intervals': False,
              'decoding_expectation_estimated': False,
              'row_count': len(ids),
              'ordered_row_ids_sha256': hashlib.sha256(json.dumps(ids, separators=(',', ':')).encode()).hexdigest(),
              'design_sha256': hashlib.sha256(np.asarray(x, dtype='<f8').tobytes()).hexdigest(),
              'human_contrast': gamma_h, 'arms': {}, 'error_changes': {}}
    for name, values in model_arms.items():
        b = contrast_bounds(x, values, contrast)
        result['arms'][name] = {k: v for k, v in b.items() if k != 'contrast_weights'}
        result['arms'][name]['signed_error_bounds'] = [b['lower']-gamma_h, b['upper']-gamma_h]
        values = np.asarray(values, dtype=float)
        known = ~np.isnan(values)
        low_mean = float(np.sum(values[known])/len(values))
        high_mean = float((np.sum(values[known]) + 4000*(~known).sum())/len(values))
        result['arms'][name]['mean_allocation_bounds'] = [low_mean, high_mean]
        result['arms'][name]['mean_signed_error_bounds'] = [low_mean-float(human.mean()), high_mean-float(human.mean())]
    if 'F' in result['arms']:
        first = result['arms']['F']
        for base in ['N', 'F-I']:
            if base in result['arms']:
                b = result['arms'][base]
                result['error_changes'][f'F_minus_{base}'] = error_change_bounds(
                    [first['lower'], first['upper']], [b['lower'], b['upper']], gamma_h)
        if 'F-I' in result['arms']:
            b = result['arms']['F-I']
            result['explicit_income_input_effect_bounds'] = [first['lower']-b['upper'], first['upper']-b['lower']]
    return result
