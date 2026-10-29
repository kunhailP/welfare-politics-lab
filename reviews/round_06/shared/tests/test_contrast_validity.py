import unittest

import numpy as np

from welfare_politics.contrast_validity import contrast_bounds, verify_with_exhaustive_completions


class ContrastValidityTests(unittest.TestCase):
    def test_bounds_match_exhaustive_adversarial_completions(self):
        result = verify_with_exhaustive_completions()
        self.assertEqual(result['endpoint_completions_enumerated'], 32)

    def test_known_two_by_two_interaction(self):
        group = np.repeat([0., 1.], 8)
        recipient = np.tile(np.repeat([0., 1.], 4), 2)
        x = np.column_stack([np.ones(16), group, recipient, group * recipient])
        y = np.where(group == 0, 100 + 200 * recipient, 600 + 700 * recipient)
        result = contrast_bounds(x, y, [0, 0, 0, 1])
        # Direct cell contrast: (1300-600)-(300-100)=500.
        self.assertAlmostEqual(result['lower'], 500)
        self.assertAlmostEqual(result['upper'], 500)

    def test_entirely_missing_outcomes_give_range_not_point(self):
        result = contrast_bounds(np.ones((4, 1)), np.full(4, np.nan), [1])
        self.assertEqual([result['lower'], result['upper']], [0, 4000])
        self.assertFalse(result['point_identified_in_fixed_design'])

    def test_refuses_rank_deficiency(self):
        with self.assertRaises(ValueError):
            contrast_bounds(np.ones((4, 2)), np.arange(4), [0, 1])

    def test_refuses_invalid_observed_amount(self):
        with self.assertRaises(ValueError):
            contrast_bounds(np.ones((4, 1)), [100, 100, -1, 6000], [1])

    def test_refuses_unbounded_action_space(self):
        with self.assertRaises(ValueError):
            contrast_bounds(np.eye(2), [100, np.nan], [0, 1], lower=-np.inf, upper=np.inf)


if __name__ == '__main__':
    unittest.main()
