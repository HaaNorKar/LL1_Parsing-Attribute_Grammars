import unittest
from src.g1_parser import *

class TestGrammar(unittest.TestCase):
    """
    Test class for verifying the grammar parser implemented in g1_parser.py.
    """

    def _check_analyze(self, input_string, valid):
        """
        Helper method to validate the parsing of a given input string.

        :param input_string: The string to be parsed.
        :param valid: Expected validity of the input (True for valid, False for invalid).
        """
        try:
            # Attempt to parse the input string using the parser.
            result = parser.parse(input_string)
            # Assert that the result matches the expected validity.
            assert(result == valid)
        except:
            # If an exception occurs, assert that the input was expected to be invalid.
            assert(not valid)

    def test_case_1(self):
        """
        Test Case 1: Valid input with balanced symbols.
        """
        self._check_analyze("aabbccc", True)

    def test_case_2(self):
        """
        Test Case 2: Invalid input with insufficient 'c' symbols.
        """
        self._check_analyze("aabbcc", False)

    def test_case_3(self):
        """
        Test Case 3: Invalid input with incorrect symbol order.
        """
        self._check_analyze("bbaaccc", False)

    def test_case_4(self):
        """
        Test Case 4: Invalid input with random incorrect structure.
        """
        self._check_analyze("accb", False)

    def test_case_5(self):
        """
        Test Case 5: Valid input with minimal structure.
        """
        self._check_analyze("c", True)

    def test_case_6(self):
        """
        Additional test battery
        """
        self._check_analyze("aaaaaaaaaabbbbbbbbbbccccccccccc",True) # Long chain
        self._check_analyze("abc",False) # Equal amounts
        self._check_analyze("ccab",False) # Correct amounts, wrong order
        self._check_analyze("cccccccc",True) # Only Cs
        self._check_analyze("aabb",False) # No Cs
        self._check_analyze("abbccc",False) # Mismatched n values
        self._check_analyze("aaabbcccc",False) # Too many As
        self._check_analyze("baacccc",False) # Wrong order, incorrect amount of As
        self._check_analyze("cbbbaaaa",False) # Wrong order, incorrect amounts
        self._check_analyze("abaaabbccc",False) # Start of chain is wrong, rest is right
        self._check_analyze("aabbcccabc",False) # Start of chain is right, ending is wrong

if __name__ == '__main__':
    # Run the tests when the script is executed directly.
    unittest.main()
