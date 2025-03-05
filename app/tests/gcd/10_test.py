import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_different_lengths_common_prefix(self):
        self.assertEqual(gcdOfStrings("ABABABAB", "ABAB"), "ABAB")

if __name__ == "__main__":
    unittest.main()
