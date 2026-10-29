import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile

from welfare_politics.ingest import EXPECTED_FILES, ingest


class IngestionTests(unittest.TestCase):
    def make_archive(self, root, extra=None):
        archive = root / 'source.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for name in EXPECTED_FILES:
                z.writestr(name, f'test fixture: {name}')
            if extra:
                z.writestr(extra, 'not a legitimate source member')
        return archive, hashlib.sha256(archive.read_bytes()).hexdigest()

    def test_source_can_be_reingested_without_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive, digest = self.make_archive(root)
            first = ingest(archive, root / 'raw', digest)
            second = ingest(archive, root / 'raw', digest)
            self.assertEqual(first, second)
            self.assertEqual(len(first['files']), 7)

    def test_source_drift_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive, _ = self.make_archive(root)
            with self.assertRaises(ValueError):
                ingest(archive, root / 'raw', '0' * 64)
            self.assertFalse((root / 'raw').exists())

    def test_zip_traversal_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive, digest = self.make_archive(root, '../outside')
            with self.assertRaises(ValueError):
                ingest(archive, root / 'raw', digest)
            self.assertFalse((root / 'outside').exists())
            self.assertFalse((root / 'raw').exists())

    def test_existing_raw_data_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive, digest = self.make_archive(root)
            raw = root / 'raw'; raw.mkdir(); (raw / 'study1.tab').write_text('different source')
            with self.assertRaises(ValueError):
                ingest(archive, raw, digest)
            self.assertEqual((raw / 'study1.tab').read_text(), 'different source')
            self.assertEqual(len(list(raw.iterdir())), 1)


if __name__ == '__main__':
    unittest.main()
