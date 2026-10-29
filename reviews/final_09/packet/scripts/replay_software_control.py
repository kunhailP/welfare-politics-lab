"""Exercise keyed replay with copied human values. NOT model-generated evidence.

This evaluation-only script may read outcomes. Never mount it or the reference
store in a respondent model's generation environment.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from welfare_politics.recorded_responses import IDENTITY, evaluate_recorded
from welfare_politics.render import load_jsonl


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--design', type=Path, required=True)
    p.add_argument('--requests', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    d = np.load(args.design, allow_pickle=False)
    rows = d['row_ids'].tolist()
    human = dict(zip(rows, d['y']))
    requests = load_jsonl(args.requests)
    attempts = []
    for request in requests:
        answer = {slot: int(human[f"{request['agent_id']}:{number}"])
                  for slot, number in zip(['A', 'B'], request['profile_numbers'])}
        attempts.append({**{k: request[k] for k in IDENTITY}, 'attempt': 1, 'status': 'reply',
                         'raw_reply': json.dumps(answer),
                         'returned_model_id': 'SOFTWARE_CONTROL_NOT_A_MODEL', 'cost_usd': 0})
    np.random.default_rng(20261029).shuffle(attempts)
    report = evaluate_recorded(d['x'], d['y'], d['contrast'], rows, requests, attempts,
                               'SOFTWARE_CONTROL_NOT_A_MODEL')
    for arm in report['arms'].values():
        np.testing.assert_allclose(arm['signed_error_bounds'], [0, 0], atol=1e-8)
    report.update(status='copied_human_keyed_replay_SOFTWARE_CONTROL_ONLY', actual_model_calls=0,
                  empirical_model_results=False)
    (args.output / 'receipt.json').write_text(json.dumps(report, indent=2))
    print('PASS keyed copied-reference software control; actual model calls=0')


if __name__ == '__main__':
    main()
