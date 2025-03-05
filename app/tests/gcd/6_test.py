import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(gcdOfStrings("", "ABC"), "")

if __name__ == "__main__":
    unittest.main()
