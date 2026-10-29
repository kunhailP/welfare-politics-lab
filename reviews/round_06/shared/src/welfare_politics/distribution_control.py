"""Outcome-informed permutation controls preserving exact lower-order tables.

These are evaluation software controls, never real model responses or a new
theorem. Greedy disjoint checkerboard swaps have no optimality certificate.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np

from .contrast_validity import contrast_bounds
from .diagnostic_comparison import compare, layout


def construct(x, human, contrast):
    base, group = layout(x)
    human = np.asarray(human, float)
    if human.shape != (len(base),) or not np.isfinite(human).all() or not ((human >= 0) & (human <= 4000)).all() or not np.equal(human, np.floor(human)).all():
        raise ValueError('Fully observed bounded integer human reference required')
    weights = contrast_bounds(x, human, contrast)['contrast_weights']
    cells = defaultdict(lambda: {0: [], 1: []})
    for i, row in enumerate(base):
        cells[tuple(row)][int(group[i])].append(i)
    pairs = defaultdict(list)
    for profile, cell in cells.items():
        for high in cell[0]:
            for low in cell[1]:
                a, b = int(human[high]), int(human[low])
                if a != b:
                    pairs[(a, b)].append((profile, high, low))
    candidates = []
    for (a, b), records in pairs.items():
        for profile, high, low in records:
            for other, other_high, other_low in pairs.get((b, a), []):
                if profile == other or (high, low) >= (other_high, other_low):
                    continue
                gain = float((a-b)*(weights[low]-weights[high]-weights[other_low]+weights[other_high]))
                candidates.append((gain, (high, low, other_high, other_low)))
    controls = {}
    for direction, name in [(1, 'increase'), (-1, 'decrease')]:
        values, used, cycles = human.astype(np.int64).copy(), set(), 0
        for gain, indices in sorted(candidates, key=lambda item: (-direction*item[0], item[1])):
            if direction*gain <= 1e-10 or used.intersection(indices):
                continue
            high, low, other_high, other_low = indices
            values[high], values[low] = values[low], values[high]
            values[other_high], values[other_low] = values[other_low], values[other_high]
            used.update(indices); cycles += 1
        assert np.array_equal(np.sort(values), np.sort(human))
        for g in [0, 1]:
            assert np.array_equal(np.sort(values[group == g]), np.sort(human[group == g]))
        for cell in cells.values():
            indices = cell[0]+cell[1]
            assert np.array_equal(np.sort(values[indices]), np.sort(human[indices]))
        diagnostics = compare(x, human, values)
        assert diagnostics['global_allocation_w1_cad']['upper'] < 1e-8
        assert diagnostics['respondent_group_weighted_w1_cad']['upper'] < 1e-8
        assert diagnostics['pooled_complete_profile_weighted_w1_cad']['upper'] < 1e-8
        controls[name] = {'values': values, 'contrast': float(weights@values), 'cycles': cycles,
                          'changed_rows': int(np.count_nonzero(values != human)),
                          'diagnostic_comparison': diagnostics}
    receipt = {'status': 'outcome_informed_permutation_SOFTWARE_CONTROL_ONLY',
               'actual_model_calls': 0, 'empirical_model_results': False,
               'human_contrast': float(weights@human), 'candidate_cycles': len(candidates),
               'sharp_extremum_certified': False,
               'has_changed_contrast_control': any(abs(control['contrast']-float(weights@human)) > 1e-8 for control in controls.values()),
               'preserved_exactly': ['overall allocation multiset', 'each income-group allocation multiset',
                                     'each pooled complete-recipient-profile allocation multiset',
                                     'fixed additive design X-transpose-y, allocation sum of squares, OLS coefficients and R2 when defined'],
               'not_preserved': ['group-by-profile outcome tables', 'individual trajectories',
                                 'relationships to respondent facts outside the primary design'],
               'scope': 'Specified lower-order checks only; stronger conditional checks can detect the control. No external benchmark-wide failure or real generator error established.'}
    return controls, receipt


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--design', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    d = np.load(args.design, allow_pickle=False)
    controls, receipt = construct(d['x'], d['y'], d['contrast'])
    np.savez(args.output/'permutation_controls_NOT_MODEL_OUTPUTS.npz',
             **{key: control['values'] for key, control in controls.items()})
    receipt['controls'] = {key: {k: v for k, v in control.items() if k != 'values'}
                           for key, control in controls.items()}
    (args.output/'receipt.json').write_text(json.dumps(receipt, indent=2))
    print(json.dumps({k: receipt[k] for k in ['status', 'actual_model_calls', 'human_contrast', 'candidate_cycles']}, indent=2))


if __name__ == '__main__':
    main()
