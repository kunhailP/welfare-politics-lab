import json
from pathlib import Path
import tempfile
import unittest

from welfare_politics.render import ARMS, common_task_plan, plan


class ScheduleTests(unittest.TestCase):
    def fixture(self, root):
        profile = {'vignette_gender': 'Female', 'vignette_ethnicity': 'South Asian',
                   'vignette_health': 'Healthy', 'vignette_citizen': 'Not a citizen',
                   'vignette_marital': 'Married', 'vignette_children': 'No children',
                   'vignette_employment': 'Employed full-time', 'vignette_income': '$60,000'}
        full = []
        for i, phase in enumerate(['pilot', 'pilot', 'confirmatory', 'confirmatory']):
            full.append({'agent_id': f's1:{i}', 'phase': phase,
                         'observed_socioeconomic_facts': {'respondent_income': 'Low income' if i % 2 else 'High income',
                             'respondent_children': 'No children', 'respondent_employment': 'Not at risk'}})
        for arm in ARMS:
            (root / arm).mkdir()
            rows = []
            for a in full:
                facts = dict(a['observed_socioeconomic_facts'])
                if arm == 'no_persona': facts = {}
                if arm.endswith('without_income'): facts.pop('respondent_income', None)
                rows.append({**a, 'observed_socioeconomic_facts': facts})
            (root / arm / 'agents.jsonl').write_text('\n'.join(json.dumps(a) for a in rows))
        profiles = [{'agent_id': a['agent_id'], 'task_number': number, 'recipient_attributes': dict(profile)}
                    for a in full for number in [1, 2, 3, 4]]
        (root / 'recipient_profiles.jsonl').write_text('\n'.join(json.dumps(a) for a in profiles))

    def test_schedule_reproduces_and_interleaves_all_arms_by_pair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            a, b = plan(root), plan(root)
            self.assertEqual(a, b)
            self.assertEqual(len(a), 12)
            for start in range(0, len(a), 3):
                block = a[start:start+3]
                self.assertEqual({r['arm'] for r in block}, set(ARMS))
                self.assertEqual(len({(r['agent_id'], tuple(r['profile_numbers'])) for r in block}), 1)

    def test_common_task_crosses_six_inputs_per_base_without_human_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            rows = common_task_plan(root, bases=2)
            self.assertEqual(len(rows), 12)
            for base in [0, 1]:
                cells = {(r['income_label'], r['focal_income']) for r in rows if r['audit_base'] == base}
                self.assertEqual(len(cells), 6)
            self.assertTrue(all('human' not in json.dumps(r['messages']).lower() for r in rows))
            for r in rows:
                self.assertEqual(r['focal_position'], 'B' if r['audit_base'] % 2 else 'A')

    def test_corrupted_arm_ablations_duplicates_and_missing_agents_rejected(self):
        mutations = [('no_persona', 'respondent_income', 'Low income'),
                     ('socioeconomic_persona_without_income', 'respondent_income', 'Low income'),
                     ('socioeconomic_persona_without_income', 'respondent_children', 'Children'),
                     ('socioeconomic_persona_without_income', 'respondent_employment', 'At risk/laid off')]
        for arm, field, value in mutations:
            with self.subTest(field=field, arm=arm), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); self.fixture(root)
                path = root / arm / 'agents.jsonl'
                rows = [json.loads(line) for line in path.read_text().splitlines()]
                rows[2]['observed_socioeconomic_facts'][field] = value
                path.write_text('\n'.join(json.dumps(r) for r in rows))
                with self.assertRaises(ValueError): plan(root)
        for duplicate in [True, False]:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); self.fixture(root)
                path = root / 'no_persona/agents.jsonl'
                rows = path.read_text().splitlines()
                rows = rows+[rows[2]] if duplicate else rows[:2]+rows[3:]
                path.write_text('\n'.join(rows))
                with self.assertRaises(ValueError): plan(root)

    def test_same_name_profiles_are_explicitly_distinct_people(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            rows = plan(root)
            self.assertTrue(all(r['same_canonical_name'] for r in rows))
            self.assertTrue(all('distinct hypothetical people' in r['messages'][1]['content'] for r in rows))


if __name__ == '__main__':
    unittest.main()
