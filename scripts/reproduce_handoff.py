"""Reproduce the delivered offline project from the separate source archive.

Installation happens separately. This command has no network or model-call path.
It never starts pilot/main generation and never overwrites an existing run.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True, help='Original separately supplied dataverse.zip')
    p.add_argument('--output', type=Path, required=True, help='New run directory; never reused')
    args = p.parse_args()
    repo = Path(__file__).resolve().parents[1]
    archive = args.archive.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    for name in ['OPENAI_API_KEY', 'SV_LLM_API_KEY', 'ANTHROPIC_API_KEY', 'GH_TOKEN', 'GITHUB_TOKEN']:
        env.pop(name, None)
    env['PYTHONPATH'] = str(repo / 'src')
    env['OPENBLAS_NUM_THREADS'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    cohort = output / 'core/prepared_inputs/evaluation_reference/cohort_linkage.tsv'
    steps = [
        ('source_ingest', ['-m', 'welfare_politics.ingest', '--archive', str(archive)]),
        ('core', ['scripts/reproduce.py', '--output', str(output / 'core')]),
        ('source_sensitivity', ['scripts/audit_human_reference_stability.py', '--cohort', str(cohort),
                                '--output', str(output / 'source_sensitivity')]),
        ('statistical_references', ['-m', 'welfare_politics.statistical_references', '--cohort', str(cohort),
                                     '--output', str(output / 'statistical_references')]),
        ('tests', ['-m', 'unittest', 'discover', '-s', 'tests']),
    ]
    completed = []
    for name, arguments in steps:
        result = subprocess.run([sys.executable, *arguments], cwd=repo, env=env, capture_output=True, text=True)
        log = output / f'{name}.log'
        log.write_text(result.stdout + result.stderr)
        if result.returncode:
            (output / 'handoff_receipt.json').write_text(json.dumps({
                'status': 'failed', 'failed_step': name, 'completed_steps': completed,
                'log': str(log), 'actual_respondent_model_calls': 0}, indent=2))
            raise SystemExit(f'{name} failed; inspect {log}')
        completed.append(name)
        print(f'PASS {name}', flush=True)
    tests = re.search(r'Ran (\d+) tests?', (output / 'tests.log').read_text())
    artifacts = {str(f.relative_to(output)): sha256(f)
                 for f in sorted(output.rglob('*')) if f.is_file()}
    receipt = {'status': 'complete_offline_handoff_reproduction', 'completed_steps': completed,
               'actual_respondent_model_calls': 0, 'paid_generation_usd': 0,
               'source_archive_sha256': sha256(archive), 'wrapper_sha256': sha256(__file__),
               'python': sys.version.split()[0], 'tests_passed': int(tests.group(1)) if tests else None,
               'installation_performed_by_this_command': False,
               'native_socioverse_runner_included': False, 'artifacts_sha256': artifacts}
    (output / 'handoff_receipt.json').write_text(json.dumps(receipt, indent=2))
    print(f'Complete. Receipt: {output / "handoff_receipt.json"}')


if __name__ == '__main__':
    main()
