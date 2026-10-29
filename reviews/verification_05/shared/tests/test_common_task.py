import unittest

from welfare_politics.common_task import summarize


class CommonTaskTests(unittest.TestCase):
    def fixture(self, interaction=0):
        return [{'audit_base': b, 'income_label': label, 'focal_income': income,
                 'focal_position': 'B' if b % 2 else 'A',
                 'amount': 1000 + 50*b + 200*(label == 'Low income') +
                           300*(income == '$30,000') + interaction*(label == 'Low income')*(income == '$30,000')}
                for b in range(2) for label in ['High income', 'Low income', 'omitted']
                for income in ['$30,000', '$120,000']]

    def test_additive_and_interacting_tables_recover_known_equal_base_did(self):
        for effect in [0, 250]:
            report = summarize(self.fixture(effect), bases=2)
            self.assertEqual(report['contrasts']['low_minus_high_did']['lower'], effect)
            self.assertEqual(report['contrasts']['low_minus_high_did']['upper'], effect)
            self.assertEqual(report['contrasts']['omitted_recipient_contrast']['lower'], 300)
            self.assertFalse(report['human_fidelity_validation'])

    def test_missing_cell_has_bounds_without_complete_base_deletion(self):
        rows = self.fixture(250); rows[0]['amount'] = None
        report = summarize(rows, bases=2)
        bound = report['contrasts']['low_minus_high_did']
        self.assertEqual(bound['upper']-bound['lower'], 2000)
        for value in [0, 4000]:
            rows[0]['amount'] = value
            point = summarize(rows, bases=2)['contrasts']['low_minus_high_did']['lower']
            self.assertLessEqual(bound['lower'], point)
            self.assertGreaterEqual(bound['upper'], point)
        with self.assertRaises(ValueError): summarize(rows[1:], bases=2)

    def test_duplicate_unknown_and_wrong_focal_position_rejected(self):
        rows = self.fixture()
        with self.assertRaises(ValueError): summarize(rows+[rows[0]], bases=2)
        rows[0]['focal_position'] = 'B'
        with self.assertRaises(ValueError): summarize(rows, bases=2)
