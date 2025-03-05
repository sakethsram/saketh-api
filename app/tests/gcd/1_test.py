import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_common_prefix(self):
        self.assertEqual(gcdOfStrings("ABCABC", "ABC"), "ABC")

if __name__ == "__main__":
    unittest.main()
