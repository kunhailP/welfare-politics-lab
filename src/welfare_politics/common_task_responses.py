"""Keyed offline replay of the frozen common-task model-input audit."""
import argparse
import hashlib
import json
from pathlib import Path

from .common_task import INCOMES, LABELS, summarize
from .render import load_jsonl, message_digest
from .response_accounting import cost_summary, final_pair

IDENTITY = ('audit_request_id', 'audit_base', 'income_label', 'focal_income',
            'focal_position', 'messages_sha256')


def request_identity(request):
    value = {key: request[key] for key in IDENTITY if key != 'audit_request_id'}
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def validate_plan(requests, bases=16):
    expected = {(b, label, income) for b in range(bases) for label in LABELS for income in INCOMES}
    cells, keyed = set(), {}
    for request in requests:
        cell = (request['audit_base'], request['income_label'], request['focal_income'])
        if type(cell[0]) is not int or cell not in expected or cell in cells:
            raise ValueError('Unexpected or duplicate common-task cell')
        if request['focal_position'] != ('B' if cell[0] % 2 else 'A'):
            raise ValueError('Common-task focal position differs from the fixed rule')
        if message_digest(request['messages']) != request['messages_sha256']:
            raise ValueError('Common-task message hash mismatch')
        key = request_identity(request)
        if request.get('audit_request_id', key) != key or key in keyed:
            raise ValueError('Common-task request ID mismatch')
        keyed[key] = {**request, 'audit_request_id': key}
        cells.add(cell)
    if bases < 1 or cells != expected:
        raise ValueError('Common-task plan must include every frozen cell')
    return keyed


def evaluate_recorded(requests, attempts, expected_model, bases=16):
    if not isinstance(expected_model, str) or not expected_model:
        raise ValueError('An exact frozen returned-model ID is required')
    planned = validate_plan(requests, bases)
    histories = {key: [] for key in planned}
    for attempt in attempts:
        key = attempt['audit_request_id']
        if key not in planned or any(attempt.get(k) != planned[key][k] for k in IDENTITY):
            raise ValueError('Unexpected common-task log or changed cell mapping')
        histories[key].append(attempt)
    cells, failures = [], []
    for key, request in planned.items():
        parsed = final_pair(histories[key], expected_model)
        amount = None if parsed['amounts'] is None else parsed['amounts'][request['focal_position']]
        cells.append({**{k: request[k] for k in IDENTITY if k not in ('audit_request_id', 'messages_sha256')},
                      'amount': amount})
        if amount is None:
            failures.append({'audit_request_id': key, 'status': parsed['status']})
    report = summarize(cells, bases)
    report['response_linkage'] = {'planned_requests': len(planned), 'logged_attempts': len(attempts),
        'failed_pairs': failures, 'expected_returned_model_id': expected_model,
        'provider_authenticity_verified': False, **cost_summary(attempts)}
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--requests', type=Path, required=True)
    p.add_argument('--attempts', type=Path, required=True)
    p.add_argument('--expected-model', required=True)
    p.add_argument('--frozen-receipt', type=Path, required=True)
    p.add_argument('--expected-receipt-sha256', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    raw = args.frozen_receipt.read_bytes()
    if hashlib.sha256(raw).hexdigest() != args.expected_receipt_sha256:
        raise ValueError('Core receipt differs from the external pre-generation seal')
    receipt = json.loads(raw)
    plan_hash = hashlib.sha256(args.requests.read_bytes()).hexdigest()
    if receipt.get('status') != 'offline_reproduction_complete' or receipt.get('artifacts_sha256', {}).get(
            'planned_primary_requests/common_task_audit_requests.jsonl') != plan_hash:
        raise ValueError('Common-task plan differs from the frozen core receipt')
    report = evaluate_recorded(load_jsonl(args.requests), load_jsonl(args.attempts), args.expected_model)
    report['frozen_core_receipt_sha256'] = args.expected_receipt_sha256
    report['attempt_log_sha256'] = hashlib.sha256(args.attempts.read_bytes()).hexdigest()
    with args.output.open('x') as handle:
        json.dump(report, handle, indent=2)


if __name__ == '__main__':
    main()
