"""Publish the reviewed local commit to a new private repository via gh.

Default is a plan only. Authentication belongs in the user's GitHub CLI login,
never in this repository or a chat message. No force push or existing-repo reuse.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def run(args, root):
    return subprocess.run(args, cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--owner', default='kunhailP')
    p.add_argument('--name', default='welfare-politics-lab')
    p.add_argument('--execute', action='store_true')
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    destination = f'{args.owner}/{args.name}'
    if not args.execute:
        print(json.dumps({'status': 'plan_only', 'destination': destination, 'visibility': 'private',
                          'requires': 'GitHub CLI authenticated as the intended owner; clean committed repository',
                          'remote_created': False, 'files_pushed': False}, indent=2))
        return
    if not shutil.which('gh'):
        raise SystemExit('GitHub CLI is unavailable; no remote was created or pushed')
    login = run(['gh', 'api', 'user', '--jq', '.login'], root)
    if login.casefold() != args.owner.casefold():
        raise SystemExit('Authenticated account differs from destination owner; no mutation performed')
    if run(['git', 'status', '--porcelain'], root):
        raise SystemExit('Commit and review the working tree before publishing')
    tracked = run(['git', 'ls-files'], root).splitlines()
    for name in tracked:
        if name.startswith(('data/raw/', 'runs/')) or '.env' in Path(name).parts or 'evaluation_reference' in Path(name).parts:
            raise SystemExit('Tracked evaluation data or credentials found; publication aborted')
    exists = subprocess.run(['gh', 'repo', 'view', destination, '--json', 'name'], cwd=root, capture_output=True)
    if exists.returncode == 0:
        raise SystemExit('Destination already exists; inspect it instead of overwriting')
    result = run(['gh', 'repo', 'create', destination, '--private', '--source', '.', '--push',
                  '--description', 'Human-grounded evaluation of synthetic welfare politics'], root)
    print(result)


if __name__ == '__main__':
    main()
