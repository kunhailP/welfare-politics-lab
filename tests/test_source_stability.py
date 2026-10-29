import unittest

from scripts.audit_human_reference_stability import sign_counts


class SourceStabilityTests(unittest.TestCase):
    def test_roundoff_at_mathematical_zero_does_not_invent_sign_changes(self):
        counts = sign_counts([1e-13, -1e-13, 0, 1e-8, -1e-8, 3e-8, -3e-8])
        self.assertEqual(counts, {'positive_draws': 1, 'negative_draws': 1, 'zero_draws': 5})


if __name__ == '__main__':
    unittest.main()
