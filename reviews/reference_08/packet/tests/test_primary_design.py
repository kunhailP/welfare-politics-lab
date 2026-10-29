import unittest

import numpy as np
import pandas as pd

from welfare_politics.primary_design import construct
from welfare_politics.contrast_validity import contrast_bounds
from welfare_politics.study1_interest_audit import LEVELS


def source_fixture():
    rng = np.random.default_rng(18)
    n = 80 * 4
    d = pd.DataFrame({'id': np.repeat(np.arange(80), 4), 'vignette_num': np.tile([1, 2, 3, 4], 80)})
    d['respondent_income'] = np.where(d.id < 40, 'High income', 'Low income')
    d['respondent_employment'] = 'Not at risk'
    d['respondent_children'] = 'No children'
    for feature, levels in LEVELS.items():
        d[feature] = rng.choice(levels, n)
    low_person = d.respondent_income.eq('Low income')
    low_recipient = d.vignette_income.eq('$30,000')
    d['vignette_allocation'] = 800 + 200*low_person + 300*low_recipient + 150*(low_person & low_recipient)
    return d


class PrimaryDesignTests(unittest.TestCase):
    def test_all_factor_primary_target_has_36_columns(self):
        d = source_fixture()
        x, y, c, rows, meta = construct(d, list(range(80)))
        self.assertEqual(meta['design_columns'], 36)
        self.assertEqual(meta['primary_people'], 80)
        self.assertEqual(len(rows), 320)
        result = contrast_bounds(x, y, c)
        self.assertAlmostEqual(result['lower'], 150)

    def test_primary_does_not_silently_drop_one_missing_profile(self):
        d = source_fixture(); d.loc[0, 'vignette_employment'] = None
        with self.assertRaises(ValueError):
            construct(d, list(range(80)))
        # A separately declared complete-person eligibility rule removes all4.
        eligible = d[list(LEVELS)].notna().all(axis=1).groupby(d.id).all()
        ids = list(eligible[eligible].index)
        self.assertNotIn(0, ids)
        self.assertEqual(len(d[d.id.isin(ids)]), 316)

    def test_original_row_order_does_not_change_primary_hashes(self):
        d = source_fixture()
        a = construct(d, list(range(80)))[-1]
        b = construct(d.sample(frac=1, random_state=4), list(reversed(range(80))))[-1]
        for key in ['cohort_sha256', 'design_sha256', 'contrast_sha256', 'row_ids_sha256']:
            self.assertEqual(a[key], b[key])

    def test_missing_requested_person_is_rejected(self):
        with self.assertRaises(ValueError):
            construct(source_fixture(), list(range(81)))


class ProjectionCompositionTests(unittest.TestCase):
    def projection(self, counts):
        rows = []
        for group, table in enumerate(counts):
            for (a, b), n in zip([(0, 0), (0, 1), (1, 0), (1, 1)], table):
                rows.extend([(group, a, b)] * n)
        g, a, b = np.asarray(rows, dtype=float).T
        x = np.column_stack([np.ones(len(g)), a, b, g, g*a, g*b])
        y = 4000*a*b  # Deliberately group-blind nonlinear rule.
        return contrast_bounds(x, y, [0, 0, 0, 0, 1, 0])['lower']

    def test_group_blind_rule_can_have_nonzero_group_projection(self):
        self.assertAlmostEqual(self.projection([[16, 4, 16, 4], [13, 7, 13, 7]]), 600)

    def test_common_profile_distribution_removes_that_artifact(self):
        self.assertAlmostEqual(self.projection([[10, 10, 10, 10], [10, 10, 10, 10]]), 0)


if __name__ == '__main__':
    unittest.main()
