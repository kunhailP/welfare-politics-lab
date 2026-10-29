"""Descriptive matched-design evaluation of one recorded model rollout.

This module makes no superpopulation or decoding-expectation inference. The
same rows/design are used for human and all arms, including invalid-action rows.
"""
import hashlib
import json

import numpy as np

from .contrast_validity import contrast_bounds, error_change_bounds
from .diagnostic_comparison import compare, layout


def group_component_bounds(x, outcomes, contrast):
    """Components of an interaction contrast in the canonical two-block design.

    In this unrestricted fully interacted design, components depend on
    disjoint groups of outcomes; their continuous-completion joint feasible set
    is rectangular. Gamma retains its direct weights for numerical consistency.
    This property must not be assumed for other restricted/partial interactions.
    """
    base, _ = layout(x)
    c = np.asarray(contrast, float)
    p = base.shape[1]
    if c.shape != (2*p,) or np.any(c[:p]) or not np.any(c[p:]):
        raise ValueError('Expected a nonzero contrast in the interaction block only')
    high = np.r_[c[p:], np.zeros(p)]
    low = high+c
    return {name: {k: value for k, value in contrast_bounds(x, outcomes, vector).items()
                   if k != 'contrast_weights'}
            for name, vector in [('high_income', high), ('low_income', low)]}


def evaluate_arrays(x, human, model_arms, contrast, row_ids):
    """Low-level numerical API; arrays alone cannot establish response linkage.

    Real logged responses must enter through recorded_responses.evaluate_recorded.
    Non-log callers must be explicitly labelled software controls or human-
    trained statistical references, never empirical respondent-model evidence.
    """
    x = np.asarray(x, dtype=float)
    human = np.asarray(human, dtype=float)
    ids = [value.item() if isinstance(value, np.generic) else value for value in row_ids]
    if len(ids) != len(human) or len(set(ids)) != len(ids):
        raise ValueError('Row identifiers must be unique and aligned with outcomes')
    h = contrast_bounds(x, human, contrast)
    if not h['point_identified_in_fixed_design'] or h['invalid_rows']:
        raise ValueError('Primary human reference must be fully observed on the frozen design')
    gamma_h = h['lower']
    result = {'target': 'finite matched cohort, fixed design, labelled array evaluation',
              'outcome_provenance': 'Caller-labelled arrays; no response linkage established by this helper',
              'sampling_confidence_intervals': False,
              'decoding_expectation_estimated': False,
              'row_count': len(ids),
              'ordered_row_ids_sha256': hashlib.sha256(json.dumps(ids, separators=(',', ':')).encode()).hexdigest(),
              'design_sha256': hashlib.sha256(np.asarray(x, dtype='<f8').tobytes()).hexdigest(),
              'human_outcomes_sha256': hashlib.sha256(np.asarray(human, dtype='<f8').tobytes()).hexdigest(),
              'contrast_sha256': hashlib.sha256(np.asarray(contrast, dtype='<f8').tobytes()).hexdigest(),
              'human_contrast': gamma_h, 'arms': {}, 'error_changes': {}}
    try:
        human_components = group_component_bounds(x, human, contrast)
    except ValueError as exc:
        human_components = None
        result['human_group_components'] = {'status': 'unsupported_component_layout', 'reason': str(exc)}
    else:
        result['human_group_components'] = {'status': 'available', **human_components}
    for name, values in model_arms.items():
        b = contrast_bounds(x, values, contrast)
        result['arms'][name] = {k: v for k, v in b.items() if k != 'contrast_weights'}
        result['arms'][name]['signed_error_bounds'] = [b['lower']-gamma_h, b['upper']-gamma_h]
        if human_components is None:
            result['arms'][name]['group_components'] = {'status': 'unsupported_component_layout'}
        else:
            components = group_component_bounds(x, values, contrast)
            for group, bound in components.items():
                reference = human_components[group]['lower']
                bound['signed_error_bounds'] = [bound['lower']-reference, bound['upper']-reference]
            result['arms'][name]['group_components'] = {'status': 'available', **components}
        values = np.asarray(values, dtype=float)
        # The generic array helper also serves noncanonical numerical fixtures.
        # Real primary designs use canonical recipient basis + group interactions.
        try:
            layout(x)
        except ValueError as exc:
            result['arms'][name]['same_output_diagnostics'] = {'status': 'unsupported_diagnostic_layout', 'reason': str(exc)}
        else:
            result['arms'][name]['same_output_diagnostics'] = compare(x, human, values)
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
