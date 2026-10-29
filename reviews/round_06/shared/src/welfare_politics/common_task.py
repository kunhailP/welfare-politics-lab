"""Finite equal-base model-only counterfactual contrasts, with completion bounds."""
LABELS = ['High income', 'Low income', 'omitted']
INCOMES = ['$30,000', '$120,000']


def summarize(records, bases=16):
    cells = {}
    for r in records:
        key = (r['audit_base'], r['income_label'], r['focal_income'])
        if key in cells or type(key[0]) is not int or key[0] not in range(bases) or key[1] not in LABELS or key[2] not in INCOMES:
            raise ValueError('Duplicate or unexpected common-task cell')
        if r['focal_position'] != ('B' if key[0] % 2 else 'A'):
            raise ValueError('Common-task focal position differs from frozen rule')
        value = r['amount']
        if value is not None and (type(value) is not int or not 0 <= value <= 4000):
            raise ValueError('Invalid actions require an explicit None marker')
        cells[key] = value
    expected = {(b, label, income) for b in range(bases) for label in LABELS for income in INCOMES}
    if bases < 1 or set(cells) != expected:
        raise ValueError('Every planned cell requires an outcome or explicit invalid marker')
    definitions = {'high_recipient_contrast': {'High income': 1},
                   'low_recipient_contrast': {'Low income': 1},
                   'omitted_recipient_contrast': {'omitted': 1},
                   'low_minus_high_did': {'Low income': 1, 'High income': -1},
                   'low_minus_omitted_did': {'Low income': 1, 'omitted': -1},
                   'high_minus_omitted_did': {'High income': 1, 'omitted': -1}}
    bounds = {}
    for name, coefficients in definitions.items():
        low = high = missing_weight = 0.
        for (base, label, income), value in cells.items():
            weight = coefficients.get(label, 0) * (1 if income == INCOMES[0] else -1) / bases
            if value is None:
                low += min(0, 4000*weight); high += max(0, 4000*weight)
                missing_weight += abs(weight)
            else:
                low += weight*value; high += weight*value
        bounds[name] = {'lower': low, 'upper': high, 'missing_absolute_weight': missing_weight}
    return {'target': 'finite equal-base counterfactual input contrasts; one recorded rollout',
            'human_fidelity_validation': False, 'sampling_confidence_intervals': False,
            'expected_generator_behavior_estimated': False,
            'bases': bases, 'invalid_cells': sum(v is None for v in cells.values()), 'contrasts': bounds}
