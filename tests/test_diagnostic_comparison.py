from itertools import product
import unittest

import numpy as np

from welfare_politics.diagnostic_comparison import compare, w1_completion_bounds


class DiagnosticTests(unittest.TestCase):
    def fixture(self):
        r = np.tile(np.repeat([0., 1.], 2), 2)
        g = np.repeat([0., 1.], 4)
        b = np.column_stack([np.ones(8), r])
        return np.column_stack([b, b*g[:, None]])

    def test_identical_outcomes_have_zero_distances_and_projection_difference(self):
        x, y = self.fixture(), np.arange(8)*200
        report = compare(x, y, y)
        for key in ['global_allocation_w1_cad', 'respondent_group_weighted_w1_cad',
                    'pooled_complete_profile_weighted_w1_cad', 'group_by_profile_weighted_w1_cad']:
            self.assertEqual(report[key]['lower'], 0)
            self.assertEqual(report[key]['upper'], 0)
        self.assertAlmostEqual(report['additive_projection']['max_absolute_coefficient_difference'], 0)

    def test_missing_actions_keep_fixed_cells_and_bounds_cover_grid_completions(self):
        x = self.fixture(); human = np.array([0, 1000, 4000, 2000, 500, 3000, 1500, 4000])
        actions = human.astype(float); actions[[0, 4]] = np.nan
        bounded = compare(x, human, actions)
        self.assertEqual(bounded['full_row_count'], 8)
        self.assertEqual(bounded['invalid_rows'], 2)
        self.assertEqual(bounded['additive_projection']['status'], 'not_computed_with_invalid_actions')
        self.assertTrue(np.isnan(actions[[0, 4]]).all())
        for completion in product([0, 1000, 2000, 3000, 4000], repeat=2):
            completed = actions.copy(); completed[[0, 4]] = completion
            exact = compare(x, human, completed)
            # Refinement can mechanically enlarge a descriptive distance.
            # It does not by itself validate a population conditional estimate.
            for key in ['respondent_group_weighted_w1_cad', 'pooled_complete_profile_weighted_w1_cad']:
                self.assertLessEqual(exact['global_allocation_w1_cad']['lower'], exact[key]['lower']+1e-8)
                self.assertLessEqual(exact[key]['lower'], exact['group_by_profile_weighted_w1_cad']['lower']+1e-8)
            for key in ['global_allocation_w1_cad', 'respondent_group_weighted_w1_cad',
                        'pooled_complete_profile_weighted_w1_cad', 'group_by_profile_weighted_w1_cad']:
                self.assertLessEqual(bounded[key]['lower'], exact[key]['lower']+1e-8)
                self.assertGreaterEqual(bounded[key]['upper'], exact[key]['upper']-1e-8)

    def test_unknown_action_extrema_cannot_be_assumed_at_action_endpoints(self):
        # W1 is not convex in a labelled unknown action: the middle can be worse.
        ref = [0, 4000]
        bound = w1_completion_bounds(ref, [2000, np.nan])
        interior = w1_completion_bounds(ref, [2000, 2000])['lower']
        endpoint = w1_completion_bounds(ref, [2000, 0])['lower']
        self.assertGreater(interior, endpoint)
        self.assertLessEqual(bound['lower'], interior)
        self.assertGreaterEqual(bound['upper'], interior)
        self.assertFalse(bound['sharp_bounds_certified'])

    def test_constant_reference_r2_is_undefined_not_perfect(self):
        report = compare(self.fixture(), np.full(8, 2000), np.full(8, 2000))
        self.assertIsNone(report['additive_projection']['human_r2'])
        self.assertIsNone(report['additive_projection']['actions_r2'])
        cells = report['group_by_profile_weighted_w1_cad']
        self.assertEqual(cells['cell_size_histogram'], {'2': 4})
        self.assertEqual(cells['singleton_row_fraction'], 0)

    def test_unequal_cells_use_row_weights_and_keep_invalid_singleton(self):
        r = np.array([0]+[1]*3+[0]*2+[1]*5, float)
        g = np.array([0]*4+[1]*7, float)
        base = np.column_stack([np.ones(11), r])
        x = np.column_stack([base, base*g[:, None]])
        human = np.full(11, 1000.)
        actions = np.array([1200]+[1400]*3+[1600]*2+[1800]*5, float)
        exact = compare(x, human, actions)['group_by_profile_weighted_w1_cad']
        self.assertAlmostEqual(exact['lower'], 6600/11)
        self.assertEqual(exact['cell_size_histogram'], {'1': 1, '2': 1, '3': 1, '5': 1})
        actions[0] = np.nan
        bounded = compare(x, human, actions)['group_by_profile_weighted_w1_cad']
        self.assertEqual(bounded['cells'], 4)
        self.assertAlmostEqual(bounded['singleton_row_fraction'], 1/11)
        self.assertAlmostEqual(bounded['lower'], 6400/11)
        self.assertAlmostEqual(bounded['upper'], 9400/11)

    def test_unbounded_or_infinite_actions_rejected(self):
        for values in [[-1, 1000], [4001, 1000], [np.inf, 1000]]:
            with self.assertRaises(ValueError): w1_completion_bounds([0, 1000], values)
