import json
import unittest

from welfare_politics.render import FACT_TEXT, messages, parse_pair


class RenderTests(unittest.TestCase):
    def setUp(self):
        profile = {'vignette_gender': 'Male', 'vignette_ethnicity': 'White',
                   'vignette_health': 'Poor health', 'vignette_citizen': 'Citizen born in Canada',
                   'vignette_marital': 'Single', 'vignette_children': 'No children',
                   'vignette_employment': 'Unemployed', 'vignette_income': '$30,000'}
        self.pair = [profile, {**profile, 'vignette_income': '$120,000'}]
        self.facts = {'respondent_income': 'Low income', 'respondent_employment': 'At risk/laid off', 'respondent_children': 'Children'}

    def test_income_ablation_changes_only_income_sentence(self):
        full = messages(self.facts, self.pair)
        omitted = messages({k: v for k, v in self.facts.items() if k != 'respondent_income'}, self.pair)
        self.assertEqual(full[0], omitted[0])
        self.assertEqual(full[1]['content'].replace(FACT_TEXT['respondent_income']['Low income']+'\n', '', 1), omitted[1]['content'])

    def test_missing_income_gives_identical_f_and_f_i_messages(self):
        facts = {k: v for k, v in self.facts.items() if k != 'respondent_income'}
        self.assertEqual(messages(facts, self.pair), messages(dict(facts), self.pair))

    def test_human_outcome_cannot_be_rendered_as_fact(self):
        with self.assertRaises(ValueError):
            messages({**self.facts, 'vignette_allocation': 2000}, self.pair)
        pair = [{**self.pair[0], 'vignette_allocation': 2000}, self.pair[1]]
        with self.assertRaises(ValueError): messages({}, pair)

    def test_no_arm_label_or_history_in_messages(self):
        rendered = messages({}, self.pair)
        text = json.dumps(rendered)
        self.assertNotIn('socioeconomic_persona', text)
        self.assertEqual([m['role'] for m in rendered], ['system', 'user'])
        self.assertIn('pre-existing condition', text)
        self.assertNotIn('annual individual income', text)
        self.assertIn('income before the pandemic', text)

    def test_strict_pair_parser_rejects_malformed_or_partial_answers(self):
        for raw in ['{"A":1,"B":2.0}', '{"A":true,"B":2}', '{"A":1}',
                    '{"A":1,"A":2,"B":3}', '{"A":-1,"B":3}',
                    '{"A":1,"B":4001}', 'Answer: {"A":1,"B":2}',
                    '{"A":1,"B":2,"reason":"x"}']:
            with self.subTest(raw=raw):
                result = parse_pair(raw)
                self.assertEqual(result['status'], 'invalid')
                self.assertIsNone(result['amounts'])

    def test_separate_valid_amounts_need_not_sum_to_4000(self):
        result = parse_pair('{"A":4000,"B":4000}')
        self.assertEqual(result['status'], 'valid')


if __name__ == '__main__':
    unittest.main()
