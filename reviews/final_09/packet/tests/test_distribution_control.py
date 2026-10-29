import unittest

import numpy as np

from welfare_politics.distribution_control import construct


class DistributionControlTests(unittest.TestCase):
    def fixture(self):
        r = np.tile(np.repeat([0., 1.], 2), 2)
        g = np.repeat([0., 1.], 4)
        base = np.column_stack([np.ones(8), r])
        x = np.column_stack([base, base*g[:, None]])
        y = np.array([0, 0, 4000, 4000, 4000, 4000, 0, 0])
        return x, y, [0, 0, 0, 1]

    def test_exact_distributions_and_additive_fit_survive_interaction_reversal(self):
        x, y, c = self.fixture()
        controls, receipt = construct(x, y, c)
        self.assertAlmostEqual(receipt['human_contrast'], -8000)
        self.assertAlmostEqual(controls['increase']['contrast'], 8000)
        control = controls['increase']; report = control['diagnostic_comparison']
        for key in ['global_allocation_w1_cad', 'respondent_group_weighted_w1_cad',
                    'pooled_complete_profile_weighted_w1_cad']:
            self.assertEqual(report[key]['upper'], 0)
        self.assertGreater(report['group_by_profile_weighted_w1_cad']['lower'], 0)
        np.testing.assert_array_equal(np.sort(y), np.sort(control['values']))
        proj = report['additive_projection']
        self.assertAlmostEqual(proj['human_r2'], proj['actions_r2'])
        self.assertAlmostEqual(proj['max_absolute_coefficient_difference'], 0)
        self.assertFalse(receipt['empirical_model_results'])
        self.assertFalse(receipt['sharp_extremum_certified'])

    def test_all_zero_reference_cannot_create_a_changed_contrast(self):
        x, y, c = self.fixture()
        controls, receipt = construct(x, np.zeros(8), c)
        self.assertFalse(receipt['has_changed_contrast_control'])
        self.assertTrue(all(control['changed_rows'] == 0 for control in controls.values()))

    def test_noninteger_reference_and_invalid_design_rejected(self):
        x, y, c = self.fixture()
        y = y.astype(float); y[0] = .5
        with self.assertRaises(ValueError): construct(x, y, c)
        x[0, 3] = 1
        with self.assertRaises(ValueError): construct(x, np.zeros(8), c)
