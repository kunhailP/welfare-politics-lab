import unittest

import numpy as np
import pandas as pd

from welfare_politics.human_audit import clean_study2


class PublishedCleaningTests(unittest.TestCase):
    def test_ties_at_cutoff_can_exclude_more_than_two_percent(self):
        values = np.tile(np.r_[np.full(96, 100.), np.full(4, 5000.)], 2)
        source = pd.DataFrame({'id': np.repeat(np.arange(50), 4),
                               'duration': 100., 'condition': np.repeat(['COVID-19', 'GST'], 100),
                               'vignette_allocation': values})
        result, audit = clean_study2(source)
        self.assertEqual(audit['strict_condition_98th_percentile_cutoffs'], {'COVID-19': 5000., 'GST': 5000.})
        self.assertEqual(len(result), 192)
        # Constant allocations are not silently removed as "straightlining".
        self.assertTrue(result.vignette_allocation.eq(100).all())
        self.assertEqual(len(source), 200)


if __name__ == '__main__':
    unittest.main()
