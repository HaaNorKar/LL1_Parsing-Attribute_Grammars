import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFirst(unittest.TestCase):
    """
    Test class to verify the computation of First sets in a grammar.
    """

    def _check_first(
            self,
            grammar: Grammar,
            input_string: str,
            first_set: AbstractSet[str],
    ) -> None:
        """
        Helper method to check the First set for a given input string.

        :param grammar: The Grammar object.
        :param input_string: The input string for which the First set is being computed.
        :param first_set: The expected First set as a set of strings.
        """
        with self.subTest(
                string=f"First({input_string}), expected {first_set}",
        ):
            # Compute the First set for the input string using the grammar.
            computed_first = grammar.compute_first(input_string)
            # Assert that the computed First set matches the expected one.
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """
        Test Case 1: Verify First set computation for a sample grammar.
        The grammar includes nullable productions and terminals.
        """
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        # Parse the grammar string to create a Grammar object.
        grammar = GrammarFormat.read(grammar_str)

        # Verify First sets for various grammar symbols and input strings.
        self._check_first(grammar, "E", {'(', 'i'})  # First(E) = { '(', 'i' }
        self._check_first(grammar, "T", {'(', 'i'})  # First(T) = { '(', 'i' }
        self._check_first(grammar, "X", {'', '+'})  # First(X) = { '', '+' }
        self._check_first(grammar, "Y", {'', '*'})  # First(Y) = { '', '*' }
        self._check_first(grammar, "", {''})  # First(ε) = { '' }
        self._check_first(grammar, "Y+i", {'+', '*'})  # First(Y+i) = { '+', '*' }
        self._check_first(grammar, "YX", {'+', '*', ''})  # First(YX) = { '+', '*', '' }
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})  # First(YXT) = { '+', '*', 'i', '(' }

    def test_case2(self) -> None:
        """
        Test Case 2: Verify First set computation for a grammar with nullable productions.
        The grammar includes multiple nullable rules.
        """
        grammar_str = """
        S -> AB
        A -> aA
        A ->
        B -> bB
        B ->
        """

        # Parse the grammar string to create a Grammar object.
        grammar = GrammarFormat.read(grammar_str)

        # Verify First sets for various grammar symbols and input strings.
        self._check_first(grammar, "S", {'a', 'b', ''})  # First(S) = { 'a', 'b', '' }
        self._check_first(grammar, "A", {'a', ''})  # First(A) = { 'a', '' }
        self._check_first(grammar, "B", {'b', ''})  # First(B) = { 'b', '' }
        self._check_first(grammar, "AB", {'a', 'b', ''})  # First(AB) = { 'a', 'b', '' }
        self._check_first(grammar, "AAB", {'a', 'b', ''})  # First(AAB) = { 'a', '' }
        self._check_first(grammar, "aB", {'a'})  # First(aB) = { 'a' }

    def test_case3(self) -> None:
        """
        Additional test battery
        """
        grammar_str = """
        R -> AfP
        A -> a
        A -> R*P
        A ->
        P -> fQ
        P -> *aA
        P ->
        Q -> a*P
        Q -> ZQ
        Z -> R
        Z -> S
        S -> b
        S -> e
        """

        # Parse the grammar string to create a Grammar object.
        grammar = GrammarFormat.read(grammar_str)

        self._check_first(grammar, "R", {'a','f'})

if __name__ == '__main__':
    # Run the tests when the script is executed directly.
    unittest.main()
