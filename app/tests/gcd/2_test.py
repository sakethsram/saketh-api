import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_no_common_divisor(self):
        self.assertEqual(gcdOfStrings("ABABAB", "ABAB"), "AB")

if __name__ == "__main__":
    unittest.main()
