"""One-command offline reproduction; no network or model-call code path."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

from welfare_politics.contrast_validity import verify_with_exhaustive_completions


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path('data/raw'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--bootstrap', type=int, default=500)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    for key in ['OPENAI_API_KEY', 'SV_LLM_API_KEY', 'ANTHROPIC_API_KEY', 'GITHUB_TOKEN', 'GH_TOKEN']:
        env.pop(key, None)
    env['OPENBLAS_NUM_THREADS'] = '1'
    steps = [('human_audit', 'study2_human', ['--bootstrap', str(args.bootstrap)]),
             ('study1_interest_audit', 'study1_adjusted', []),
             ('design_diagnostics', 'design_diagnostics', []),
             ('prepare_design', 'prepared_inputs', [])]
    for module, folder, extra in steps:
        command = [sys.executable, '-m', f'welfare_politics.{module}', '--source', str(args.source),
                   '--output', str(args.output / folder), *extra]
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        (args.output / f'{folder}.log').write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{module} failed; see {folder}.log')
        print(f'PASS {folder}', flush=True)
    cohort = args.output / 'prepared_inputs/evaluation_reference/cohort_linkage.tsv'
    result = subprocess.run([sys.executable, '-m', 'welfare_politics.primary_design',
                             '--source', str(args.source), '--cohort', str(cohort),
                             '--output', str(args.output / 'primary_matched_design')],
                            env=env, capture_output=True, text=True)
    (args.output / 'primary_matched_design.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('Primary design failed; see primary_matched_design.log')
    print('PASS primary_matched_design', flush=True)
    result = subprocess.run([sys.executable, '-m', 'welfare_politics.render',
                             '--inputs', str(args.output / 'prepared_inputs/generation_inputs'),
                             '--output', str(args.output / 'planned_primary_requests')],
                            env=env, capture_output=True, text=True)
    (args.output / 'planned_primary_requests.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('Request plan failed; see planned_primary_requests.log')
    print('PASS planned_primary_requests', flush=True)
    result = subprocess.run([sys.executable, '-m', 'welfare_politics.failure_budget',
                             '--design', str(args.output / 'primary_matched_design/human_reference_design.npz'),
                             '--output', str(args.output / 'failure_budget')],
                            env=env, capture_output=True, text=True)
    (args.output / 'failure_budget.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('Failure budget audit failed; see failure_budget.log')
    print('PASS failure_budget', flush=True)
    result = subprocess.run([sys.executable, 'scripts/replay_software_control.py',
                             '--design', str(args.output / 'primary_matched_design/human_reference_design.npz'),
                             '--requests', str(args.output / 'planned_primary_requests/requests.jsonl'),
                             '--output', str(args.output / 'keyed_software_replay')],
                            env=env, capture_output=True, text=True)
    (args.output / 'keyed_software_replay.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('Keyed software replay failed; see keyed_software_replay.log')
    print('PASS keyed_software_replay (not model evidence)', flush=True)
    verification = verify_with_exhaustive_completions()
    (args.output / 'contrast_software_check.json').write_text(json.dumps(verification, indent=2))
    generated = {str(x.relative_to(args.output)): hashlib.sha256(x.read_bytes()).hexdigest()
                 for x in sorted(args.output.rglob('*')) if x.is_file()}
    receipt = {'status': 'offline_reproduction_complete', 'new_model_calls': 0,
               'new_paid_spend': 0, 'human_data_reanalysis': True,
               'real_model_results': False,
               'python': sys.version.split()[0],
               'packages': {name: importlib.metadata.version(name) for name in ['numpy', 'pandas', 'scipy']},
               'artifacts_sha256': generated}
    (args.output / 'receipt.json').write_text(json.dumps(receipt, indent=2))
    print('PASS offline_reproduction_complete; new model calls=0')


if __name__ == '__main__':
    main()
