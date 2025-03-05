import unittest
from gcd_of_strings import gcdOfStrings

class TestGCDOfStrings(unittest.TestCase):
    def test_identical_large_strings(self):
        self.assertEqual(gcdOfStrings("XYZXYZXYZXYZ", "XYZXYZXYZXYZ"), "XYZXYZXYZXYZ")

if __name__ == "__main__":
    unittest.main()
