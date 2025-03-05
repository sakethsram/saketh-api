import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_same_strings(self):
        self.assertEqual(gcdOfStrings("ABC", "ABC"), "ABC")

if __name__ == "__main__":
    unittest.main()
