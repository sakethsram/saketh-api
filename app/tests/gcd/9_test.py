import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_one_character_repeated(self):
        self.assertEqual(gcdOfStrings("BBBBBB", "BB"), "BB")

if __name__ == "__main__":
    unittest.main()
