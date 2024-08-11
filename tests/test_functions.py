
import unittest
from lib.utility.functions import normalize_score, calculate_composite_score

class TestFunctions(unittest.TestCase):

    def test_normalize_score(self):
        # Normal case
        self.assertAlmostEqual(normalize_score(50, 0, 100), 0.5)
        self.assertAlmostEqual(normalize_score(75, 0, 100), 0.75)

        # Edge cases
        self.assertAlmostEqual(normalize_score(0, 0, 100), 0.0)
        self.assertAlmostEqual(normalize_score(100, 0, 100), 1.0)

        # Case where min_val equals max_val (should handle divide-by-zero)
        with self.assertRaises(ZeroDivisionError):
            normalize_score(50, 100, 100)
            
if __name__ == '__main__':
    unittest.main()
