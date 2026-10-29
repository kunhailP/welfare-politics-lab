import unittest

import numpy as np
import pandas as pd

from welfare_politics.primary_design import matrix_and_contrast
from welfare_politics.statistical_references import fit_predict, person_folds
from welfare_politics.study1_interest_audit import LEVELS


def fixture(start, people, seed):
    rng = np.random.default_rng(seed)
    d = pd.DataFrame({'id': np.repeat(np.arange(start, start+people), 4),
                      'vignette_num': np.tile([1, 2, 3, 4], people),
                      'respondent_income': np.repeat(np.where(np.arange(people) % 2, 'Low income', 'High income'), 4)})
    for feature, levels in LEVELS.items():
        d[feature] = rng.choice(levels, len(d))
    g = d.respondent_income.eq('Low income').to_numpy(float)
    poor = d.vignette_income.eq('$30,000').to_numpy(float)
    d['vignette_allocation'] = 1200+200*g+300*poor+150*g*poor
    return d


class StatisticalReferenceTests(unittest.TestCase):
    def test_training_recovers_known_out_of_person_conditional_means(self):
        train, target = fixture(0, 200, 1), fixture(1000, 80, 2)
        pred, meta = fit_predict(train, target.drop(columns='vignette_allocation'), 'B_income_interacted_OLS')
        np.testing.assert_allclose(pred, target.vignette_allocation, atol=1e-8)
        self.assertEqual(meta['rank'], 36)

    def test_target_labels_and_id_values_cannot_change_fitted_predictions(self):
        train, target = fixture(0, 200, 1), fixture(1000, 80, 2)
        altered = target.copy()
        altered['vignette_allocation'] = -1e9
        altered['id'] = altered.id+10000
        for name in ['B_mean', 'B_recipient_OLS', 'B_income_interacted_OLS']:
            with self.subTest(name=name):
                first, fit1 = fit_predict(train, target, name)
                second, fit2 = fit_predict(train, altered, name)
                np.testing.assert_array_equal(first, second)
                self.assertEqual(fit1, fit2)
        with self.assertRaisesRegex(ValueError, 'overlap'):
            fit_predict(train, train.iloc[:8], 'B_mean')

    def test_person_folds_partition_ids_and_never_split_their_rows(self):
        train = fixture(0, 202, 1)
        folds = person_folds(train, 20261030, 5)
        self.assertEqual(set.union(*folds), set(train.id))
        self.assertEqual(sum(map(len, folds)), train.id.nunique())
        for ids in folds:
            self.assertTrue(train[train.id.isin(ids)].groupby('id').size().eq(4).all())
        self.assertEqual(folds, person_folds(train, 20261030, 5))

    def test_additive_prediction_has_zero_interaction_under_unbalanced_tasks(self):
        train, target = fixture(0, 200, 1), fixture(1000, 80, 2)
        predicted, _ = fit_predict(train, target, 'B_recipient_OLS')
        x, c = matrix_and_contrast(target)
        gamma = c @ np.linalg.lstsq(x, predicted, rcond=None)[0]
        self.assertAlmostEqual(gamma, 0, places=8)


if __name__ == '__main__':
    unittest.main()
