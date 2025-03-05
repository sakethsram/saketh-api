import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_partial_overlap_but_no_gcd(self):
        self.assertEqual(gcdOfStrings("ABCDAB", "ABCD"), "")

if __name__ == "__main__":
    unittest.main()
