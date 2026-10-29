"""Verified local-only ingestion of the specific user-provided source archive."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

EXPECTED_SHA256 = '06e74a2df4c0e9b7382ffcacc6d1844cae0b450c07a165b8046620f52c3b8625'
EXPECTED_FILES = {'study1.tab', 'study2.tab', 'study2_alt.tab', 'main.Rmd',
                  'README.md', 'renv.lock', 'deservingness.Rproj'}


def ingest(archive, destination, expected_sha256=EXPECTED_SHA256):
    archive, destination = Path(archive), Path(destination)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != expected_sha256:
        raise ValueError('Source archive hash differs; verify/version provenance before ingestion')
    staged = {}
    with zipfile.ZipFile(archive) as z:
        items = z.infolist()
        if len({i.filename for i in items}) != len(items):
            raise ValueError('Duplicate archive entries')
        if sum(i.file_size for i in items) > 50_000_000:
            raise ValueError('Unexpected expanded archive size')
        for i in items:
            if i.filename not in EXPECTED_FILES or i.is_dir():
                raise ValueError('Unexpected source member; no extraction performed')
            if ((i.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError('Archive symlink rejected')
            staged[i.filename] = z.read(i)
    if set(staged) != EXPECTED_FILES:
        raise ValueError('Incomplete source archive')
    # Validate all conflicts before any writes.
    for name, data in staged.items():
        path = destination / name
        if path.is_symlink():
            raise ValueError('Destination symlink rejected')
        if path.exists() and path.read_bytes() != data:
            raise ValueError('Existing source differs; use a new destination')
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in staged.items():
        (destination / name).write_bytes(data)
    return {'archive_sha256': digest, 'source': 'doi:10.7910/DVN/LPHMB7',
            'licensing': 'External-data redistribution not independently verified',
            'files': {k: {'bytes': len(v), 'sha256': hashlib.sha256(v).hexdigest()}
                      for k, v in sorted(staged.items())}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--destination', type=Path, default=Path('data/raw'))
    p.add_argument('--receipt', type=Path, default=Path('data/source_receipt.json'))
    args = p.parse_args()
    result = ingest(args.archive, args.destination)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2))
    print(json.dumps({'status': 'source_verified', 'files': len(result['files']),
                      'archive_sha256': result['archive_sha256']}, indent=2))


if __name__ == '__main__':
    main()
