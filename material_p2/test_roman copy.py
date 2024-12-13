import unittest
from src.roman_parser import *

class TestRomanGrammar(unittest.TestCase):
    """
    Test class for verifying the Roman numeral grammar parser implemented in roman_parser.py.
    """

    def _check_analyze(self, input_string, int_value, valid):
        """
        Helper method to validate the parsing of a Roman numeral input.

        :param input_string: The Roman numeral string to be parsed.
        :param int_value: The expected integer value for valid Roman numerals.
        :param valid: Expected validity of the input (True for valid, False for invalid).
        """
        # Parse the input string using the parser.
        result = parser.parse(input_string)
        if not result["valid"]:
            # If the result indicates invalid input, assert the expected validity is False.
            assert(not valid)
        else:
            # If the result is valid, check that the parsed value matches the expected integer value.
            assert(result["val"] == int_value)

    def test_case_1(self):
        """
        Test Case 1: Invalid input with an incorrect sequence.
        """
        self._check_analyze("XX", 20, False)

    def test_case_2(self):
        """
        Test Case 2: Valid input for a Roman numeral.
        """
        self._check_analyze("IX", 9, True)

    def test_case_3(self):
        """
        Test Case 3: Valid input for a Roman numeral with multiple symbols.
        """
        self._check_analyze("XII", 12, True)

    def test_case_4(self):
        """
        Test Case 4: Invalid input with excessive repetition of symbols.
        """
        self._check_analyze("XIIII", 13, False)

    def test_case_5(self):
        """
        Test Case 5: Valid input for the smallest Roman numeral.
        """
        self._check_analyze("I", 1, True)

    def test_case_6(self):
        """
        Test Case 6: Valid input for a Roman numeral with subtractive notation.
        """
        self._check_analyze("XL", 40, True)

    def test_case_7(self):
        """
        Test Case 7: Invalid input with mixed-up symbols.
        """
        self._check_analyze("IVX", -1, False)

    def test_case_8(self):
        """
        Test Case 8: Valid input for a complex Roman numeral.
        """
        self._check_analyze("CMXCIX", 999, True)


if __name__ == '__main__':
    # Run the tests when the script is executed directly.
    unittest.main()
