import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from welfare_politics.common_task_responses import IDENTITY, evaluate_recorded, request_identity as audit_id
from welfare_politics.platform_bundle import export_bundle
from welfare_politics.render import ARMS, message_digest, request_identity
from welfare_politics.response_accounting import cost_entry, cost_summary


def common_fixture(bases=2):
    requests, attempts = [], []
    for base in range(bases):
        for label in ('High income', 'Low income', 'omitted'):
            for income in ('$30,000', '$120,000'):
                messages = [{'role': 'system', 'content': 'SOFTWARE TEST ONLY'},
                            {'role': 'user', 'content': f'TEST {base}/{label}/{income}'}]
                r = {'audit_base': base, 'income_label': label, 'focal_income': income,
                     'focal_position': 'B' if base % 2 else 'A', 'messages': messages,
                     'messages_sha256': message_digest(messages), 'interpretation': 'software test only'}
                requests.append(r)
                focal = 1000 + 300*(income == '$30,000') + 250*(label == 'Low income' and income == '$30,000')
                answer = {'A': 37, 'B': 37}; answer[r['focal_position']] = focal
                a = {k: r[k] for k in IDENTITY if k != 'audit_request_id'}
                attempts.append({**a, 'audit_request_id': audit_id(r), 'attempt': 1,
                    'status': 'reply', 'returned_model_id': 'SOFTWARE_TEST_ONLY',
                    'raw_reply': json.dumps(answer), 'cost_value': .25, 'cost_unit': 'SocioVerse_Sim'})
    return requests, attempts


class AccountingTests(unittest.TestCase):
    def test_usd_compatibility_and_credit_units_never_invent_exchange_rate(self):
        self.assertEqual(cost_summary([{'cost_usd': .5}])['logged_cost_usd'], .5)
        s = cost_summary([{'cost_value': 2, 'cost_unit': 'SocioVerse_Sim'},
                          {'cost_value': 3, 'cost_unit': 'SocioVerse_Agent'}, {'cost_usd': .5}])
        self.assertEqual(s['logged_cost_by_unit'], {'USD': .5, 'SocioVerse_Agent': 3, 'SocioVerse_Sim': 2})
        self.assertIsNone(s['logged_cost_usd'])
        self.assertFalse(s['credit_to_usd_conversion_performed'])

    def test_unknown_ambiguous_nonfinite_and_negative_costs_fail(self):
        cases = [{}, {'cost_usd': None}, {'cost_usd': True}, {'cost_usd': -1},
                 {'cost_usd': float('nan')}, {'cost_usd': float('inf')}, {'cost_usd': 10**1000},
                 {'cost_value': 1, 'cost_unit': 'invented_unit'},
                 {'cost_value': 1, 'cost_unit': []}, {'cost_usd': 0, 'cost_value': 2, 'cost_unit': 'USD'}]
        for case in cases:
            with self.subTest(case=str(case)[:80]):
                with self.assertRaises(ValueError): cost_entry(case)


class CommonLogTests(unittest.TestCase):
    def setUp(self):
        self.requests, self.attempts = common_fixture()

    def score(self, attempts=None, requests=None):
        return evaluate_recorded(self.requests if requests is None else requests,
            self.attempts if attempts is None else attempts, 'SOFTWARE_TEST_ONLY', bases=2)

    def test_keyed_shuffled_replay_respects_alternating_focal_ab(self):
        a = self.score()
        b = self.score(list(reversed(self.attempts)), list(reversed(self.requests)))
        self.assertEqual(a, b)
        self.assertEqual(a['contrasts']['low_minus_high_did']['lower'], 250)
        self.assertEqual(a['contrasts']['low_minus_high_did']['upper'], 250)
        self.assertEqual(a['response_linkage']['logged_cost_by_unit'], {'SocioVerse_Sim': 3})
        self.assertIsNone(a['response_linkage']['logged_cost_usd'])
        self.assertFalse(a['human_fidelity_validation'])

    def test_wrong_cell_prompt_model_id_and_focal_position_fail(self):
        for key, value in [('audit_base', 99), ('income_label', 'Low income'),
                           ('focal_position', 'B'), ('messages_sha256', 'bad'),
                           ('returned_model_id', 'wrong'), ('audit_request_id', 'bad')]:
            changed = copy.deepcopy(self.attempts); changed[0][key] = value
            with self.subTest(key=key):
                with self.assertRaises(ValueError): self.score(changed)
        changed = copy.deepcopy(self.requests); changed[0]['messages'][0]['content'] = 'changed'
        with self.assertRaises(ValueError): self.score(requests=changed)

    def test_missing_duplicate_logs_and_incomplete_or_duplicate_plan_fail(self):
        for attempts in (self.attempts[1:], self.attempts+[self.attempts[0]]):
            with self.assertRaises(ValueError): self.score(attempts)
        for requests in (self.requests[1:], self.requests+[self.requests[0]]):
            with self.assertRaises(ValueError): self.score(requests=requests)

    def test_invalid_nonfocal_reply_invalidates_pair_and_keeps_all_bases(self):
        changed = copy.deepcopy(self.attempts); changed[0]['raw_reply'] = '{"A":1000,"B":true}'
        report = self.score(changed)
        self.assertEqual(report['invalid_cells'], 1)
        bounds = report['contrasts']['low_minus_high_did']
        self.assertEqual(bounds['upper']-bounds['lower'], 2000)
        with self.assertRaises(ValueError): self.score(changed + [{**changed[0], 'attempt': 2}])

    def test_exhausted_transport_and_retry_histories_are_explicit(self):
        changed = copy.deepcopy(self.attempts)
        changed[0].update(status='transport_error', raw_reply=None, returned_model_id=None)
        with self.assertRaises(ValueError): self.score(changed)
        changed += [{**changed[0], 'attempt': 2}, {**changed[0], 'attempt': 3}]
        self.assertEqual(self.score(changed)['invalid_cells'], 1)
        changed[-1]['attempt'] = True
        with self.assertRaises(ValueError): self.score(changed)


class GenerationExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.core = self.root/'core'
        plans = self.core/'planned_primary_requests'; plans.mkdir(parents=True)
        self.primary = []
        for arm in ARMS:
            for pair in ([1, 2], [3, 4]):
                messages = [{'role':'system','content':'SOFTWARE TEST ONLY'}, {'role':'user','content':'TEST'}]
                r = {'agent_id':'TEST_PERSON','arm':arm,'profile_numbers':pair,'rollout':0,
                     'messages':messages,'messages_sha256':message_digest(messages),
                     'same_canonical_name':False,'status':'planned_only_no_model_response'}
                r['request_id'] = request_identity(r); self.primary.append(r)
        self.common, _ = common_fixture(16)
        (self.core/'human_reference_secret.txt').write_text('HUMAN_OUTCOME_SECRET_NOT_FOR_GENERATION')
        self.freeze()

    def freeze(self):
        artifacts = {}
        for name, rows in [('requests.jsonl', self.primary), ('common_task_audit_requests.jsonl', self.common)]:
            p = self.core/'planned_primary_requests'/name
            p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            artifacts[str(p.relative_to(self.core))] = hashlib.sha256(p.read_bytes()).hexdigest()
        raw = json.dumps({'status':'offline_reproduction_complete','artifacts_sha256':artifacts}).encode()
        (self.core/'receipt.json').write_bytes(raw); self.seal = hashlib.sha256(raw).hexdigest()

    def test_export_contains_only_declared_inputs_and_preserves_primary_bytes(self):
        output, archive = self.root/'bundle', self.root/'bundle.zip'
        report = export_bundle(self.core, output, self.seal, archive)
        expected = {'primary_requests.jsonl','common_task_requests.jsonl','README.txt','campaign.template.json','manifest.json'}
        self.assertEqual({p.name for p in output.iterdir()}, expected)
        self.assertEqual((output/'primary_requests.jsonl').read_bytes(),
                         (self.core/'planned_primary_requests/requests.jsonl').read_bytes())
        self.assertFalse(report['human_outcomes_included'])
        with zipfile.ZipFile(archive) as z:
            self.assertEqual(set(z.namelist()),expected)
            self.assertTrue(all(b'HUMAN_OUTCOME_SECRET' not in z.read(n) for n in z.namelist()))
        before = archive.read_bytes()
        with self.assertRaises(FileExistsError): export_bundle(self.core, output, self.seal, archive)
        self.assertEqual(archive.read_bytes(),before)

    def test_stale_external_seal_and_changed_plan_are_rejected(self):
        with self.assertRaises(ValueError): export_bundle(self.core,self.root/'a','bad')
        p=self.core/'planned_primary_requests/requests.jsonl';p.write_text(p.read_text()+'\n')
        with self.assertRaises(ValueError): export_bundle(self.core,self.root/'b',self.seal)
        self.assertFalse((self.root/'b').exists())

    def test_even_self_resealed_extra_outcome_fields_are_rejected(self):
        for target in ('primary','common'):
            rows = getattr(self,target);rows[0]['human_outcome']=2000;self.freeze()
            with self.subTest(target=target):
                with self.assertRaises(ValueError): export_bundle(self.core,self.root/target,self.seal)
            del rows[0]['human_outcome']

    def test_missing_arm_or_common_cell_is_not_exported(self):
        for target in ('primary','common'):
            rows=getattr(self,target);last=rows.pop();self.freeze()
            with self.subTest(target=target):
                with self.assertRaises(ValueError): export_bundle(self.core,self.root/target,self.seal)
            rows.append(last)
