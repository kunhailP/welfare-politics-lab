"""Design-only ambiguity under random and contrast-leverage-concentrated failures."""
import argparse
import json
from pathlib import Path

import numpy as np

from .contrast_validity import contrast_bounds


def diagnose(x, contrast, row_ids, fractions=(0.005, 0.01, 0.02, 0.05, 0.10), seed=20261029):
    weights = contrast_bounds(x, np.full(len(row_ids), np.nan), contrast)['contrast_weights']
    pairs = {}
    for i, key in enumerate(row_ids):
        study, person, task = key.split(':')
        pair = (study, person, (int(task)-1)//2)
        pairs.setdefault(pair, []).append(i)
    blocks = list(pairs.values())
    if any(len(block) != 2 for block in blocks):
        raise ValueError('Expected complete paired requests')
    leverage = np.array([np.abs(weights[block]).sum() for block in blocks])
    rng = np.random.default_rng(seed)
    rows = []
    for fraction in fractions:
        n = max(1, int(np.ceil(fraction*len(blocks))))
        random = rng.choice(len(blocks), n, replace=False)
        worst = np.argsort(leverage)[-n:]
        rows.append({'planned_invalid_pair_fraction': fraction, 'invalid_pairs': n,
                     'actual_pair_fraction': n/len(blocks),
                     'one_seeded_random_failure_completion_width_cad': float(4000*leverage[random].sum()),
                     'uniform_subset_expected_completion_width_cad': float(4000*n/len(blocks)*leverage.sum()),
                     'highest_leverage_failure_completion_width_cad': float(4000*leverage[worst].sum())})
    return {'status': 'design_only_failure_scenarios_not_model_results', 'actual_model_calls': 0,
            'pairs_per_arm': len(blocks), 'total_absolute_contrast_weight': float(np.abs(weights).sum()),
            'rows': rows,
            'interpretation': 'Width=(4000-0)*sum(abs(w_missing)); these are identification ranges, not confidence intervals. Larger N need not reduce ambiguity at a fixed invalid fraction.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--design', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    d = np.load(args.design)
    report = diagnose(d['x'], d['contrast'], list(d['row_ids']))
    (args.output / 'audit.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
