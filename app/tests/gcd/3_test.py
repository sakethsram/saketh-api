import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_no_gcd(self):
        self.assertEqual(gcdOfStrings("LEET", "CODE"), "")

if __name__ == "__main__":
    unittest.main()

