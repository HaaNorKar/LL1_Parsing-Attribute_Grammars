import unittest

from src.g1_parser import *

class TestGrammar(unittest.TestCase):
    def _check_analyze(self, input_string, valid):
        try:
            result = parser.parse(input_string)
            assert(result == valid)
        except:
            assert(not valid)

    def test_case_1(self):
        self._check_analyze("aabbccc", True)

    def test_case_2(self):
        self._check_analyze("aabbcc", False)

    def test_case_3(self):
        self._check_analyze("bbaaccc", False)

    def test_case_4(self):
        self._check_analyze("accb", False)
    
    def test_case_5(self):
        self._check_analyze("c", True)

if __name__ == '__main__':
    unittest.main()
