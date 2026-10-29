from itertools import product
import unittest

import numpy as np

from welfare_politics.contrast_validity import contrast_bounds, error_change_bounds
from welfare_politics.paired_evaluation import evaluate_arrays as evaluate


class PairedEvaluationTests(unittest.TestCase):
    def setUp(self):
        g = np.repeat([0., 1.], 8)
        r = np.tile(np.repeat([0., 1.], 4), 2)
        self.x = np.column_stack([np.ones(16), g, r, g*r])
        self.y = 200 + 300*g + 400*r + 250*g*r
        self.c = [0, 0, 0, 1]

    def test_copied_human_fixture_has_zero_discrepancy(self):
        report = evaluate(self.x, self.y, {'N': self.y, 'F': self.y, 'F-I': self.y},
                          self.c, [f'fixture:{i}' for i in range(16)])
        for arm in report['arms'].values():
            np.testing.assert_allclose(arm['signed_error_bounds'], [0, 0], atol=1e-8)
        for change in report['error_changes'].values():
            self.assertAlmostEqual(change['lower'], 0)
            self.assertAlmostEqual(change['upper'], 0)
        self.assertFalse(report['sampling_confidence_intervals'])

    def test_joint_row_permutation_preserves_contrasts(self):
        order = np.random.default_rng(3).permutation(16)
        a = evaluate(self.x, self.y, {'F': self.y+10}, self.c, list(range(16)))
        b = evaluate(self.x[order], self.y[order], {'F': self.y[order]+10}, self.c, list(order))
        self.assertAlmostEqual(a['human_contrast'], b['human_contrast'])
        np.testing.assert_allclose(a['arms']['F']['signed_error_bounds'], b['arms']['F']['signed_error_bounds'], atol=1e-8)

    def test_zero_weight_missingness_is_point_identified(self):
        x = [[1, 0], [1, 0], [0, 1]]
        b = contrast_bounds(x, [10, 20, np.nan], [1, 0])
        self.assertAlmostEqual(b['lower'], 15)
        self.assertAlmostEqual(b['upper'], 15)
        self.assertTrue(b['point_identified_in_fixed_design'])

    def test_error_change_bounds_cover_exhaustive_arm_completions(self):
        a, b = self.y.copy(), self.y.copy()
        a[[0, 8]] = np.nan
        b[[1, 9]] = np.nan
        ba, bb = contrast_bounds(self.x, a, self.c), contrast_bounds(self.x, b, self.c)
        h = contrast_bounds(self.x, self.y, self.c)['lower']
        bound = error_change_bounds([ba['lower'], ba['upper']], [bb['lower'], bb['upper']], h)
        for choices in product([0., 4000.], repeat=4):
            aa, ab = a.copy(), b.copy(); aa[[0, 8]] = choices[:2]; ab[[1, 9]] = choices[2:]
            ga = contrast_bounds(self.x, aa, self.c)['lower']
            gb = contrast_bounds(self.x, ab, self.c)['lower']
            difference = abs(ga-h)-abs(gb-h)
            self.assertGreaterEqual(difference+1e-8, bound['lower'])
            self.assertLessEqual(difference-1e-8, bound['upper'])

    def test_strong_ill_conditioning_is_rejected(self):
        x = [[1, 1], [1, 1+1e-12], [1, 1-1e-12]]
        with self.assertRaises(ValueError):
            contrast_bounds(x, [100, 100, 100], [0, 1])

    def test_mean_matching_oracle_does_not_match_the_interaction(self):
        constant = np.full(16, self.y.mean())
        report = evaluate(self.x, self.y, {'F': constant}, self.c, list(range(16)))
        np.testing.assert_allclose(report['arms']['F']['mean_signed_error_bounds'], [0, 0], atol=1e-8)
        np.testing.assert_allclose(report['arms']['F']['signed_error_bounds'], [-250, -250], atol=1e-8)


if __name__ == '__main__':
    unittest.main()
