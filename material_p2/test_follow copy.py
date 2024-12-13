import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    """
    Test class to verify the computation of Follow sets in a grammar.
    """

    def _check_follow(
            self,
            grammar: Grammar,
            symbol: str,
            follow_set: AbstractSet[str],
    ) -> None:
        """
        Helper method to check the Follow set for a given grammar symbol.

        :param grammar: The Grammar object.
        :param symbol: The grammar symbol (non-terminal) for which the Follow set is computed.
        :param follow_set: The expected Follow set as a set of strings.
        """
        with self.subTest(string=f"Follow({symbol}), expected {follow_set}"):
            # Compute the Follow set for the symbol using the grammar.
            computed_follow = grammar.compute_follow(symbol)
            # Assert that the computed Follow set matches the expected one.
            self.assertEqual(computed_follow, follow_set)

    # def test_case1(self) -> None:
    #     """
    #     Test Case 1: Verify Follow set computation for a sample grammar.
    #     This grammar includes nullable productions and interactions between non-terminals.
    #     """
    #     grammar_str = """
    #     E -> TX
    #     X -> +E
    #     X ->
    #     T -> iY
    #     T -> (E)
    #     Y -> *T
    #     Y ->
    #     """

    #     # Parse the grammar string to create a Grammar object.
    #     grammar = GrammarFormat.read(grammar_str)

    #     # Verify Follow sets for various non-terminal symbols.
    #     self._check_follow(grammar, "E", {'$', ')'})  # Follow(E) = { '$', ')' }
    #     self._check_follow(grammar, "T", {'$', ')', '+'})  # Follow(T) = { '$', ')', '+' }
    #     self._check_follow(grammar, "X", {'$', ')'})  # Follow(X) = { '$', ')' }
    #     self._check_follow(grammar, "Y", {'$', ')', '+'})  # Follow(Y) = { '$', ')', '+' }

    # def test_case2(self) -> None:
    #     """
    #     Test Case 2: Verify Follow set computation for a grammar with multiple interactions.
    #     This grammar includes nullable productions and recursive structures.
    #     """
    #     grammar_str = """
    #     S -> AB
    #     A -> aA
    #     A ->
    #     B -> bB
    #     B ->
    #     """

    #     # Parse the grammar string to create a Grammar object.
    #     grammar = GrammarFormat.read(grammar_str)

    #     # Verify Follow sets for various non-terminal symbols.
    #     self._check_follow(grammar, "S", {'$'})  # Follow(S) = { '$' }
    #     self._check_follow(grammar, "A", {'b', '$'})  # Follow(A) = { 'b', '$' }
    #     self._check_follow(grammar, "B", {'$'})  # Follow(B) = { '$' }
    #     self._check_follow(grammar, "A", {'b', '$'})  # Follow(A) = { 'b', '$' }

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

        self._check_follow(grammar, "R", {'*', 'a', 'f', 'b', 'e', '$'})


if __name__ == '__main__':
    # Run the tests when the script is executed directly.
    unittest.main()
