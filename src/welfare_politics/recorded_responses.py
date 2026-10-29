"""Offline, keyed replay of logged primary responses; no generation code.

Arrival order never determines design order. An absent log is an accounting
error, not a silently imputed refusal. Exhausted transport attempts must be
explicit. This validates internal consistency, not a provider's authenticity.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from .paired_evaluation import evaluate_arrays
from .render import ARMS, load_jsonl, message_digest, parse_pair, request_identity

ARM_LABEL = dict(zip(ARMS, ['N', 'F', 'F-I']))
IDENTITY = ['request_id', 'agent_id', 'arm', 'profile_numbers', 'rollout', 'messages_sha256']


def assemble(requests, attempts, row_ids, expected_model):
    if not isinstance(expected_model, str) or not expected_model:
        raise ValueError('An exact frozen returned-model ID is required')
    if not row_ids or len(set(row_ids)) != len(row_ids):
        raise ValueError('Expected design rows must be nonempty and unique')
    expected = set(row_ids)
    planned, occupied = {}, {arm: set() for arm in ARMS}
    for request in requests:
        key = request['request_id']
        if key in planned or request['arm'] not in ARMS or request['rollout'] != 0:
            raise ValueError('Duplicate request, unknown arm or wrong rollout')
        numbers = request['profile_numbers']
        if len(numbers) != 2 or len(set(numbers)) != 2 or any(type(n) is not int or n not in [1, 2, 3, 4] for n in numbers):
            raise ValueError('Invalid profile-number mapping')
        if message_digest(request['messages']) != request['messages_sha256'] or request_identity(request) != key:
            raise ValueError('Request content or identity digest mismatch')
        keys = {f"{request['agent_id']}:{n}" for n in numbers}
        arm = request['arm']
        if not keys <= expected or occupied[arm] & keys:
            raise ValueError('Unexpected or duplicate design row in plan')
        occupied[arm].update(keys)
        planned[key] = request
    if any(rows != expected for rows in occupied.values()):
        raise ValueError('Each arm must account for exactly the frozen design rows')
    grouped = {key: {} for key in planned}
    for attempt in attempts:
        key = attempt['request_id']
        if key not in planned:
            raise ValueError('Unknown response request ID')
        request = planned[key]
        if any(attempt.get(field) != request[field] for field in IDENTITY):
            raise ValueError('Response arm, respondent, mapping, rollout or prompt mismatch')
        number = attempt['attempt']
        if type(number) is not int or number not in [1, 2, 3] or number in grouped[key]:
            raise ValueError('Duplicate or invalid attempt number')
        cost = attempt['cost_usd']
        if type(cost) not in [int, float] or not np.isfinite(cost) or cost < 0:
            raise ValueError('Nonnegative finite per-attempt cost must be logged')
        if attempt['status'] not in ['reply', 'transport_error']:
            raise ValueError('Unknown attempt status')
        if attempt['status'] == 'reply':
            if attempt['returned_model_id'] != expected_model or not isinstance(attempt['raw_reply'], str):
                raise ValueError('Returned model differs from frozen campaign or reply is missing')
        elif attempt.get('raw_reply') is not None:
            raise ValueError('A transport failure cannot contain a model reply')
        grouped[key][number] = attempt
    aligned = {arm: {} for arm in ARMS}
    failures = []
    for key, request in planned.items():
        history = grouped[key]
        if not history or sorted(history) != list(range(1, len(history)+1)):
            raise ValueError('Missing planned log or non-contiguous retry history')
        ordered = [history[n] for n in sorted(history)]
        if any(a['status'] != 'transport_error' for a in ordered[:-1]):
            raise ValueError('Only transport errors may be retried; no duplicate final replies')
        last = ordered[-1]
        if last['status'] == 'transport_error':
            if len(ordered) != 3:
                raise ValueError('Unexhausted transport failure is not a final accounted response')
            parsed = {'status': 'transport_exhausted', 'amounts': None}
        else:
            parsed = parse_pair(last['raw_reply'])
        if parsed['amounts'] is None:
            failures.append({'request_id': key, 'arm': request['arm'], 'status': parsed['status']})
        for slot, number in zip(['A', 'B'], request['profile_numbers']):
            row = f"{request['agent_id']}:{number}"
            aligned[request['arm']][row] = np.nan if parsed['amounts'] is None else parsed['amounts'][slot]
    arrays = {ARM_LABEL[arm]: np.asarray([values[key] for key in row_ids], dtype=float)
              for arm, values in aligned.items()}
    receipt = {'alignment': 'request-keyed; explicit A/B-to-profile mapping; frozen design reindex',
               'planned_requests': len(planned), 'logged_attempts': len(attempts),
               'failed_pairs': failures, 'logged_cost_usd': sum(a['cost_usd'] for a in attempts),
               'expected_returned_model_id': expected_model,
               'provider_authenticity_verified': False}
    return arrays, receipt


def evaluate_recorded(x, human, contrast, row_ids, requests, attempts, expected_model):
    arrays, receipt = assemble(requests, attempts, row_ids, expected_model)
    report = evaluate_arrays(x, human, arrays, contrast, row_ids)
    report['response_linkage'] = receipt
    report['request_plan_sha256'] = hashlib.sha256(json.dumps(requests, sort_keys=True,
                                                            separators=(',', ':')).encode()).hexdigest()
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--design', type=Path, required=True)
    p.add_argument('--requests', type=Path, required=True)
    p.add_argument('--attempts', type=Path, required=True)
    p.add_argument('--expected-model', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    d = np.load(args.design, allow_pickle=False)
    report = evaluate_recorded(d['x'], d['y'], d['contrast'], d['row_ids'].tolist(),
                               load_jsonl(args.requests), load_jsonl(args.attempts), args.expected_model)
    report['attempt_log_sha256'] = hashlib.sha256(args.attempts.read_bytes()).hexdigest()
    # Exclusive creation preserves previously scored runs.
    with args.output.open('x') as f:
        json.dump(report, f, indent=2)


if __name__ == '__main__':
    main()
