from itertools import product
import unittest

import numpy as np

from welfare_politics.contrast_validity import contrast_bounds
from welfare_politics.paired_evaluation import evaluate_arrays, group_component_bounds


class GroupComponentTests(unittest.TestCase):
    def setUp(self):
        group = np.repeat([0., 1.], 8)
        recipient = np.tile(np.repeat([0., 1.], 4), 2)
        self.x = np.column_stack([np.ones(16), recipient, group, group*recipient])
        self.y = 1200+200*group+300*recipient+150*group*recipient
        self.c = [0, 0, 0, 1]

    def test_components_recover_both_slopes_and_their_known_difference(self):
        report = evaluate_arrays(self.x, self.y, {'F': self.y}, self.c, list(range(16)))
        components = report['arms']['F']['group_components']
        self.assertAlmostEqual(components['high_income']['lower'], 300)
        self.assertAlmostEqual(components['low_income']['lower'], 450)
        self.assertAlmostEqual(components['low_income']['lower']-components['high_income']['lower'],
                               report['arms']['F']['lower'])
        for group in ['high_income', 'low_income']:
            np.testing.assert_allclose(components[group]['signed_error_bounds'], [0, 0], atol=1e-8)

    def test_missing_component_bounds_match_exhaustive_completions(self):
        y = self.y.copy(); y[[0, 12]] = np.nan
        report = group_component_bounds(self.x, y, self.c)
        values = {'high_income': [], 'low_income': []}
        for endpoints in product([0., 4000.], repeat=2):
            full = y.copy(); full[[0, 12]] = endpoints
            beta = np.linalg.lstsq(self.x, full, rcond=None)[0]
            values['high_income'].append(beta[1])
            values['low_income'].append(beta[1]+beta[3])
        for group, endpoints in values.items():
            np.testing.assert_allclose([report[group]['lower'], report[group]['upper']],
                                       [min(endpoints), max(endpoints)], atol=1e-8)


if __name__ == '__main__':
    unittest.main()
