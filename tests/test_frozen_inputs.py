import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from welfare_politics.recorded_responses import verify_frozen_inputs


class FrozenInputTests(unittest.TestCase):
    def test_external_digest_binds_plan_and_design_even_if_plan_is_rehashed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            design, requests, receipt = [root/name for name in ['design.npz', 'requests.jsonl', 'receipt.json']]
            design.write_bytes(b'explicit software design fixture')
            requests.write_text('{"request_id":"original","messages":"original"}\n')
            sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
            receipt.write_text(json.dumps({'status': 'offline_reproduction_complete', 'artifacts_sha256': {
                'primary_matched_design/human_reference_design.npz': sha(design),
                'planned_primary_requests/requests.jsonl': sha(requests)}}))
            frozen_digest = sha(receipt)
            result = verify_frozen_inputs(design, requests, receipt, frozen_digest)
            self.assertFalse(result['model_settings_budget_bound_by_this_receipt'])
            requests.write_text('{"request_id":"new_self_consistent_hash","messages":"changed"}\n')
            with self.assertRaisesRegex(ValueError, 'Input differs'):
                verify_frozen_inputs(design, requests, receipt, frozen_digest)
            changed = json.loads(receipt.read_text())
            changed['artifacts_sha256']['planned_primary_requests/requests.jsonl'] = sha(requests)
            receipt.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, 'externally recorded digest'):
                verify_frozen_inputs(design, requests, receipt, frozen_digest)

    def test_changed_human_design_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            design, requests, receipt = [root/name for name in ['design.npz', 'requests.jsonl', 'receipt.json']]
            design.write_bytes(b'original fixture'); requests.write_text('fixture')
            sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
            receipt.write_text(json.dumps({'status': 'offline_reproduction_complete', 'artifacts_sha256': {
                'primary_matched_design/human_reference_design.npz': sha(design),
                'planned_primary_requests/requests.jsonl': sha(requests)}}))
            frozen_digest = sha(receipt)
            design.write_bytes(b'changed human labels or row layout')
            with self.assertRaisesRegex(ValueError, 'Input differs'):
                verify_frozen_inputs(design, requests, receipt, frozen_digest)
