"""Freeze a context-separated review packet without data or author documents."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--kind', choices=['fresh', 're-review', 'targeted-verification'], required=True)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    args.output.mkdir(parents=True, exist_ok=False)
    shared = args.output / 'shared'
    shared.mkdir()
    for folder in ['src', 'tests']:
        for source in sorted((root / folder).rglob('*.py')):
            target = shared / source.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for name, source in [('protocol.md', 'docs/CURRENT_PROTOCOL.md'), ('related_work.md', 'docs/RELATED_WORK.md')]:
        shutil.copyfile(root / source, shared / name)
    (shared / 'packet.md').write_text(
        '# Component-audit review packet\n\n'
        f'Type: {args.kind}. No raw data or respondent-model results are supplied.\n'
        'Read only this shared packet, its manifest and your own authorized prior report.\n'
        'Do not read parent README, AGENTS, Git metadata, other reviewer reports or raw data.\n'
        'Distinguish software verification from collection readiness and empirical novelty.\n'
        'Record prior context exposure and environment limitations honestly.\n'
        'Use PYTHONPATH=src and python -m unittest discover -s tests from this directory.\n'
    )
    hashes = {str(f.relative_to(args.output)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in sorted(shared.rglob('*')) if f.is_file()}
    (args.output / 'packet_manifest.json').write_text(json.dumps(
        {'review_type': args.kind, 'author_identity_supplied': False,
         'other_reviewer_report_supplied': False, 'raw_data_supplied': False, 'files': hashes}, indent=2))
    print(json.dumps({'status': 'packet_frozen', 'files': len(hashes), 'review_type': args.kind}))


if __name__ == '__main__':
    main()
