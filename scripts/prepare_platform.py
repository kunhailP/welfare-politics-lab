"""Prepare verified local data and a generation-only ZIP, with no model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from welfare_politics.platform_bundle import export_bundle


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--zip', dest='zip_path', type=Path, required=True)
    args = p.parse_args()
    repo = Path(__file__).resolve().parents[1]
    archive = args.archive.resolve(strict=True)
    output, zip_path = args.output.resolve(), args.zip_path.resolve()
    if output.exists() or zip_path.exists():
        raise FileExistsError('Use fresh output/ZIP paths; no prior data will be overwritten')
    output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    for key in ('OPENAI_API_KEY', 'SV_LLM_API_KEY', 'ANTHROPIC_API_KEY', 'GH_TOKEN', 'GITHUB_TOKEN'):
        env.pop(key, None)
    env['PYTHONPATH'] = str(repo/'src')
    env['OPENBLAS_NUM_THREADS'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable, 'scripts/reproduce_handoff.py',
        '--archive', str(archive), '--output', str(output/'analysis')], cwd=repo, env=env)
    if result.returncode:
        (output/'preparation_receipt.json').write_text(json.dumps({
            'status':'failed_reproduction', 'actual_model_calls':0},indent=2)+'\n')
        raise SystemExit(result.returncode)
    core = output/'analysis/core'
    seal = hashlib.sha256((core/'receipt.json').read_bytes()).hexdigest()
    manifest = export_bundle(core, output/'generation_only', seal, zip_path)
    code_paths = sorted([*repo.glob('src/**/*.py'), *repo.glob('scripts/*.py'),
        *repo.glob('configs/*.json'), repo/'pyproject.toml', repo/'requirements-tested.txt',
        repo/'docs/CURRENT_PROTOCOL.md'])
    handoff = json.loads((output/'analysis/handoff_receipt.json').read_text())
    receipt = {'status':'complete_offline_platform_input_preparation', 'actual_model_calls':0,
        'new_paid_spend':0, 'native_hosted_execution_verified':False,
        'tests_passed':handoff['tests_passed'], 'core_receipt_sha256':seal,
        'source_archive_sha256':handoff['source_archive_sha256'],
        'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),
        'generation_manifest_sha256':hashlib.sha256((output/'generation_only/manifest.json').read_bytes()).hexdigest(),
        'implementation_sha256':{str(f.relative_to(repo)):hashlib.sha256(f.read_bytes()).hexdigest() for f in code_paths},
        'primary_requests':manifest['primary_requests'], 'common_task_requests':manifest['common_task_requests'],
        'evaluation_data_path':str(output/'analysis'), 'generation_only_zip':str(zip_path)}
    (output/'preparation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(f"Prepared input-only ZIP: {zip_path}")
    print(f"Local evaluation data (keep separate): {output/'analysis'}")
    print(f"Receipt: {output/'preparation_receipt.json'}")


if __name__ == '__main__':
    main()
