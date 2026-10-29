import unittest

from welfare_politics.primary_design import estimability_diagnostic


class EstimabilityTests(unittest.TestCase):
    def test_rank_deficient_matrix_can_identify_a_specific_contrast(self):
        result = estimability_diagnostic([[1, 0], [1, 0]], [1, 0])
        self.assertFalse(result['all_coefficients_identified_full_rank'])
        self.assertTrue(result['contrast_estimable_in_design'])

    def test_contrast_outside_rowspace_is_not_identified(self):
        result = estimability_diagnostic([[1, 0], [1, 0]], [0, 1])
        self.assertFalse(result['contrast_estimable_in_design'])
        self.assertAlmostEqual(result['contrast_rowspace_residual_l2'], 1)
