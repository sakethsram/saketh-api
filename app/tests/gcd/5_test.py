import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_one_string_is_multiple_of_other(self):
        self.assertEqual(gcdOfStrings("AAAAAA", "AA"), "AA")

if __name__ == "__main__":
    unittest.main()
