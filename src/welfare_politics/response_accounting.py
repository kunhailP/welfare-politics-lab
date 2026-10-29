"""Explicit monetary/credit accounting, without exchange-rate assumptions."""
import math

UNITS = {'USD', 'SocioVerse_Agent', 'SocioVerse_Sim'}


def cost_entry(attempt):
    if 'cost_usd' in attempt:
        if 'cost_value' in attempt or 'cost_unit' in attempt:
            raise ValueError('Ambiguous USD and credit accounting fields')
        unit, value = 'USD', attempt['cost_usd']
    else:
        unit, value = attempt.get('cost_unit'), attempt.get('cost_value')
    if not isinstance(unit, str) or unit not in UNITS or type(value) not in (int, float) or value < 0:
        raise ValueError('Explicit finite nonnegative cost and a supported unit are required')
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError('Cost is not finite within supported numeric precision')
    return unit, value


def cost_summary(attempts):
    totals = {}
    for attempt in attempts:
        unit, value = cost_entry(attempt)
        totals[unit] = totals.get(unit, 0) + value
        if not math.isfinite(totals[unit]):
            raise ValueError('Accounting total overflow')
    return {'logged_cost_by_unit': dict(sorted(totals.items())),
            'logged_cost_usd': totals.get('USD') if set(totals) == {'USD'} else None,
            'credit_to_usd_conversion_performed': False,
            'provider_billing_authenticity_verified': False}


def final_pair(history, expected_model):
    """Resolve an explicit history; semantic invalidity never permits a retry."""
    from .render import parse_pair
    ordered = sorted(history, key=lambda a: a['attempt'])
    if not ordered or [a['attempt'] for a in ordered] != list(range(1, len(ordered)+1)):
        raise ValueError('Missing, duplicate or non-contiguous attempt history')
    for a in ordered:
        if type(a['attempt']) is not int or a['attempt'] not in (1, 2, 3):
            raise ValueError('Invalid attempt number')
        cost_entry(a)
        if a['status'] == 'reply':
            if a.get('returned_model_id') != expected_model or not isinstance(a.get('raw_reply'), str):
                raise ValueError('Wrong returned model or absent reply')
        elif a['status'] != 'transport_error' or a.get('raw_reply') is not None:
            raise ValueError('Invalid transport record')
    if any(a['status'] != 'transport_error' for a in ordered[:-1]):
        raise ValueError('Only transport errors may be retried')
    last = ordered[-1]
    if last['status'] == 'transport_error':
        if len(ordered) != 3:
            raise ValueError('Transport failure is not exhausted')
        return {'status': 'transport_exhausted', 'amounts': None}
    return parse_pair(last['raw_reply'])
