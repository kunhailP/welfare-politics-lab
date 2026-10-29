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
        self.assertFalse(receipt['sharp_extremum_certified'])
        self.assertTrue(receipt['has_changed_contrast_control'])
        additive = x[:, :3]
        original = np.linalg.lstsq(additive, y, rcond=None)[0]
        changed = np.linalg.lstsq(additive, controls['increase']['values'], rcond=None)[0]
        np.testing.assert_allclose(original, changed, atol=1e-8)
        # In an interacted fit the recipient main coefficient is conditional,
        # and is deliberately outside the conservation claim.
        interacted = np.linalg.lstsq(x, controls['increase']['values'], rcond=None)[0]
        self.assertAlmostEqual(interacted[1], -4000)

    def test_noninteger_reference_and_wrong_interaction_structure_rejected(self):
        x, y, c = self.fixture()
        y[0] = 1000.5
        with self.assertRaises(ValueError): construct_controls(x, y, c)
        y[0] = 1000
        x[0, 3] = 1
        with self.assertRaises(ValueError): construct_controls(x, y, c)

    def test_zero_and_cap_references_do_not_claim_a_counterexample(self):
        x, y, c = self.fixture()
        for value in [0, 4000]:
            controls, receipt = construct_controls(x, np.full(16, value), c)
            self.assertFalse(receipt['has_changed_contrast_control'])
            self.assertTrue(all(control['changed_rows'] == 0 for control in controls.values()))

    def test_no_shared_profiles_is_not_a_changed_contrast_control(self):
        rows = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
                         [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]], float)
        base = np.column_stack([np.ones(8), rows])
        group = np.repeat([0, 1], 4)
        x = np.column_stack([base, base*group[:, None]])
        c = [0, 0, 0, 0, 0, 1, 0, 0]
        controls, receipt = construct_controls(x, np.full(8, 2000), c)
        self.assertEqual(receipt['shared_profile_patterns'], 0)
        self.assertFalse(receipt['has_changed_contrast_control'])
        self.assertTrue(all(control['changed_rows'] == 0 for control in controls.values()))
