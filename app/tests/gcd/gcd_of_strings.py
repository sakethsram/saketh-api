def gcdOfStrings(str1: str, str2: str) -> str:
    """Returns the greatest common divisor (GCD) of two strings."""
    if str1 + str2 != str2 + str1:
        return ""
    from math import gcd
    return str1[:gcd(len(str1), len(str2))]
