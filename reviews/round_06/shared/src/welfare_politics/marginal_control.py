"""Integer software controls preserving group and complete-profile means.

These outcome-informed response tables are oracle diagnostics, never model
predictions or evidence of real model distortion. The greedy cycles are feasible
constructions without general sharpness certification or a novel-theorem claim.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from .contrast_validity import contrast_bounds


def construct_controls(x, human, contrast):
    x, human = np.asarray(x, float), np.asarray(human, float)
    if x.ndim != 2 or x.shape[1] % 2 or len(x) != len(human):
        raise ValueError('Expected matched main-plus-group-interaction design')
    if not np.isfinite(human).all() or not ((human >= 0) & (human <= 4000)).all() or not np.equal(human, np.floor(human)).all():
        raise ValueError('Fully observed integer human reference in 0..4000 required')
    p = x.shape[1] // 2
    base, group = x[:, :p], x[:, p]
    if not np.equal(base[:, 0], 1).all() or not np.isin(group, [0, 1]).all() or not np.array_equal(x[:, p:], base*group[:, None]):
        raise ValueError('Unexpected group-interaction construction')
    weights = contrast_bounds(x, human, contrast)['contrast_weights']
    cells = {}
    for i, (row, g) in enumerate(zip(base, group)):
        cells.setdefault(tuple(row), {0: [], 1: []})[int(g)].append(i)
    shared = [key for key, groups in cells.items() if groups[0] and groups[1]]
    gaps = {key: weights[cells[key][1][0]]-weights[cells[key][0][0]] for key in shared}
    controls = {}
    for direction in [1, -1]:
        values = human.astype(np.int64).copy()
        ordered = sorted(shared, key=lambda key: direction*gaps[key], reverse=True)
        cycles = 0
        for a in ordered:
            for b in reversed(ordered):
                if direction*(gaps[a]-gaps[b]) <= 1e-12:
                    continue
                # +low(A), +high(B), -high(A), -low(B). Pattern ordering
                # reverses the objective for decrease; do not reverse signs too.
                choices = [(cells[a][1], 1), (cells[b][0], 1), (cells[a][0], -1), (cells[b][1], -1)]
                while True:
                    selected, slack = [], []
                    for indices, sign in choices:
                        room = 4000-values[indices] if sign > 0 else values[indices]
                        position = int(np.argmax(room))
                        selected.append((indices[position], sign))
                        slack.append(int(room[position]))
                    amount = min(slack)
                    if amount == 0:
                        break
                    for i, sign in selected:
                        values[i] += sign*amount
                    cycles += 1
        # Exact integer conservation checks; do not rely on approximate means.
        for g in [0, 1]:
            assert values[group == g].sum() == human[group == g].sum()
        for groups in cells.values():
            indices = groups[0]+groups[1]
            assert values[indices].sum() == human[indices].sum()
        controls['increase' if direction == 1 else 'decrease'] = {
            'values': values, 'contrast': float(weights@values), 'cycles': cycles,
            'changed_rows': int(np.count_nonzero(values != human))}
    return controls, {'status': 'outcome_informed_integer_SOFTWARE_CONTROL_ONLY',
                      'actual_model_calls': 0, 'empirical_model_results': False,
                      'human_contrast': float(weights@human),
                      'full_recipient_profile_patterns': len(cells), 'shared_profile_patterns': len(shared),
                      'preserved_exactly': ['each respondent-group sum and mean',
                                            'each complete-recipient-profile sum and mean',
                                            'pooled recipient means and additive-regression sufficient statistics', 'grand mean'],
                      'not_preserved': ['respondent-by-recipient interactions', 'individual response trajectories',
                                        'allocation distributions or variances'],
                      'has_changed_contrast_control': any(abs(c['contrast']-float(weights@human)) > 1e-8 for c in controls.values()),
                      'sharp_extremum_certified': False,
                      'interpretation': 'A changed-contrast control is a feasible integer counterexample to identifying interaction fidelity from the listed summaries. Unchanged controls are not such evidence. No real LLM output or sharp optimization is claimed.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--design', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    d = np.load(args.design, allow_pickle=False)
    controls, receipt = construct_controls(d['x'], d['y'], d['contrast'])
    np.savez(args.output/'oracle_controls_NOT_MODEL_OUTPUTS.npz',
             **{key: control['values'] for key, control in controls.items()})
    receipt['controls'] = {key: {k: v for k, v in control.items() if k != 'values'}
                           for key, control in controls.items()}
    (args.output/'receipt.json').write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
