import copy
import json
import unittest

import numpy as np

from welfare_politics.recorded_responses import IDENTITY, assemble, evaluate_recorded
from welfare_politics.render import ARMS, message_digest, request_identity


class KeyedReplayTests(unittest.TestCase):
    def setUp(self):
        self.rows = [f's1:{i}:{j}' for i in range(4) for j in [1, 2, 3, 4]]
        g = np.repeat([0., 0., 1., 1.], 4)
        r = np.tile([0., 0., 1., 1.], 4)
        self.x = np.column_stack([np.ones(16), g, r, g*r])
        self.y = 200 + 300*g + 400*r + 250*g*r
        self.c = [0, 0, 0, 1]
        self.requests, self.attempts = [], []
        for arm in ARMS:
            for person in range(4):
                for numbers in [[1, 2], [4, 3]]:
                    request = {'agent_id': f's1:{person}', 'arm': arm, 'profile_numbers': numbers,
                               'rollout': 0, 'messages': [{'role': 'user', 'content': 'SOFTWARE FIXTURE ONLY'}]}
                    request['messages_sha256'] = message_digest(request['messages'])
                    request['request_id'] = request_identity(request)
                    self.requests.append(request)
                    answer = {slot: int(self.y[self.rows.index(f's1:{person}:{number}')])
                              for slot, number in zip(['A', 'B'], numbers)}
                    self.attempts.append({**{k: request[k] for k in IDENTITY}, 'attempt': 1,
                                          'status': 'reply', 'raw_reply': json.dumps(answer),
                                          'returned_model_id': 'fixture-only', 'cost_usd': 0})

    def score(self, attempts=None, requests=None):
        return evaluate_recorded(self.x, self.y, self.c, self.rows,
                                 self.requests if requests is None else requests,
                                 self.attempts if attempts is None else attempts, 'fixture-only')

    def test_asynchronous_order_and_reverse_ab_mapping_preserve_zero_error(self):
        shuffled = copy.deepcopy(self.attempts)
        np.random.default_rng(9).shuffle(shuffled)
        a, b = self.score(), self.score(shuffled, list(reversed(self.requests)))
        for arm in ['N', 'F', 'F-I']:
            np.testing.assert_allclose(a['arms'][arm]['signed_error_bounds'], [0, 0], atol=1e-8)
            self.assertEqual(a['arms'][arm], b['arms'][arm])
            diagnostics = a['arms'][arm]['same_output_diagnostics']
            self.assertEqual(diagnostics['global_allocation_w1_cad']['upper'], 0)
            self.assertEqual(diagnostics['group_by_profile_weighted_w1_cad']['upper'], 0)
        self.assertIn('human_outcomes_sha256', a)
        self.assertIn('contrast_sha256', a)

    def test_wrong_arm_respondent_mapping_prompt_model_or_rollout_rejected(self):
        for field, value in [('arm', ARMS[1]), ('agent_id', 's1:99'), ('profile_numbers', [2, 1]),
                             ('messages_sha256', 'bad'), ('rollout', 1), ('returned_model_id', 'other')]:
            with self.subTest(field=field):
                attempts = copy.deepcopy(self.attempts); attempts[0][field] = value
                with self.assertRaises(ValueError): self.score(attempts)

    def test_distinct_amounts_detect_ab_slot_swaps_under_shuffled_arrival(self):
        expected = np.arange(16) * 37
        attempts = copy.deepcopy(self.attempts)
        for attempt in attempts:
            answer = {slot: int(expected[self.rows.index(f"{attempt['agent_id']}:{number}")])
                      for slot, number in zip(['A', 'B'], attempt['profile_numbers'])}
            attempt['raw_reply'] = json.dumps(answer)
        np.random.default_rng(11).shuffle(attempts)
        arrays, _ = assemble(list(reversed(self.requests)), attempts, self.rows, 'fixture-only')
        for values in arrays.values():
            np.testing.assert_array_equal(values, expected)

    def test_duplicate_extra_missing_and_conflicting_attempts_fail(self):
        extra = {**self.attempts[0], 'request_id': 'unknown'}
        after_reply = {**self.attempts[0], 'attempt': 2}
        for rows in [self.attempts + [self.attempts[0]], self.attempts + [extra],
                     self.attempts[1:], self.attempts + [after_reply]]:
            with self.assertRaises(ValueError): self.score(rows)

    def test_corrupted_or_incomplete_plan_fails(self):
        requests = copy.deepcopy(self.requests); requests[0]['messages'][0]['content'] = 'changed'
        for rows in [requests, self.requests[1:], self.requests + [self.requests[0]]]:
            with self.assertRaises(ValueError): self.score(requests=rows)

    def test_invalid_pair_retains_both_rows_and_transport_retry_is_replayable(self):
        attempts = copy.deepcopy(self.attempts)
        attempts[0]['raw_reply'] = '{"A":100,"B":true}'
        reply = {**attempts[1], 'attempt': 2}
        attempts[1].update(status='transport_error', raw_reply=None, returned_model_id=None)
        attempts.append(reply)
        arrays, receipt = assemble(self.requests, attempts, self.rows, 'fixture-only')
        self.assertTrue(np.isnan(arrays['N'][:2]).all())
        self.assertEqual(np.isnan(arrays['N']).sum(), 2)
        self.assertEqual(len(receipt['failed_pairs']), 1)
        self.assertEqual(receipt['logged_attempts'], 25)
        self.assertEqual(self.score(attempts)['arms']['N']['invalid_rows'], 2)
        diagnostic = self.score(attempts)['arms']['N']['same_output_diagnostics']
        self.assertEqual(diagnostic['full_row_count'], 16)
        self.assertEqual(diagnostic['invalid_rows'], 2)
        self.assertEqual(diagnostic['group_by_profile_weighted_w1_cad']['cells'], 4)
        self.assertEqual(diagnostic['additive_projection']['status'], 'not_computed_with_invalid_actions')

    def test_transport_exhaustion_requires_all_three_attempts(self):
        attempts = copy.deepcopy(self.attempts)
        attempts[0].update(status='transport_error', raw_reply=None, returned_model_id=None)
        with self.assertRaises(ValueError): self.score(attempts)
        attempts.extend([{**attempts[0], 'attempt': n} for n in [2, 3]])
        report = self.score(attempts)
        self.assertEqual(report['arms']['N']['invalid_rows'], 2)

    def test_platform_credit_accounting_preserves_amounts_without_faking_usd(self):
        attempts = copy.deepcopy(self.attempts)
        for attempt in attempts:
            del attempt['cost_usd']
            attempt.update(cost_value=2, cost_unit='SocioVerse_Sim')
        report = self.score(attempts)
        self.assertEqual(report['response_linkage']['logged_cost_by_unit'], {'SocioVerse_Sim': 48})
        self.assertIsNone(report['response_linkage']['logged_cost_usd'])
        for arm in ('N', 'F', 'F-I'):
            self.assertEqual(report['arms'][arm], self.score()['arms'][arm])

    def test_public_replay_exposes_canonical_component_bounds(self):
        # Reorder the synthetic columns to canonical [base, base*group].
        x = self.x[:, [0, 2, 1, 3]]
        report = evaluate_recorded(x, self.y, self.c, self.rows,
                                   self.requests, self.attempts, 'fixture-only')
        self.assertIn('recorded respondent-model rollout', report['target'])
        for arm in ['N', 'F', 'F-I']:
            components = report['arms'][arm]['group_components']
            self.assertAlmostEqual(components['high_income']['lower'], 400)
            self.assertAlmostEqual(components['low_income']['lower'], 650)
            np.testing.assert_allclose(components['low_income']['signed_error_bounds'], [0, 0], atol=1e-8)


if __name__ == '__main__':
    unittest.main()
