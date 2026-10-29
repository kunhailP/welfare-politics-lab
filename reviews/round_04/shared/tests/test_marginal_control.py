import unittest

import numpy as np

from welfare_politics.marginal_control import construct_controls


class MarginalControlTests(unittest.TestCase):
    def fixture(self):
        recipient = np.tile(np.repeat([0., 1.], 4), 2)
        group = np.repeat([0., 1.], 8)
        base = np.column_stack([np.ones(16), recipient])
        return np.column_stack([base, base*group[:, None]]), np.full(16, 2000.), [0, 0, 0, 1]

    def test_full_profile_and_group_means_match_with_opposite_interactions(self):
        x, y, c = self.fixture()
        controls, receipt = construct_controls(x, y, c)
        self.assertAlmostEqual(controls['increase']['contrast'], 8000)
        self.assertAlmostEqual(controls['decrease']['contrast'], -8000)
        for control in controls.values():
            values = control['values']
            self.assertTrue(np.isin(values, [0, 4000]).all())
            for column in [1, 2]:
                for level in [0, 1]:
                    selected = x[:, column] == level
                    self.assertEqual(values[selected].mean(), y[selected].mean())
        self.assertFalse(receipt['empirical_model_results'])
        self.assertFalse(receipt['is_sharp_extremum'])

    def test_noninteger_reference_and_wrong_interaction_structure_rejected(self):
        x, y, c = self.fixture()
        y[0] = 1000.5
        with self.assertRaises(ValueError): construct_controls(x, y, c)
        y[0] = 1000
        x[0, 3] = 1
        with self.assertRaises(ValueError): construct_controls(x, y, c)
