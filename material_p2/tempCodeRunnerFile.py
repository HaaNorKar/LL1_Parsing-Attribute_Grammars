    # def test_case1(self) -> None:
    #     """
    #     Test Case 1: Verify First set computation for a sample grammar.
    #     The grammar includes nullable productions and terminals.
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

    #     # Verify First sets for various grammar symbols and input strings.
    #     self._check_first(grammar, "E", {'(', 'i'})  # First(E) = { '(', 'i' }
    #     self._check_first(grammar, "T", {'(', 'i'})  # First(T) = { '(', 'i' }
    #     self._check_first(grammar, "X", {'', '+'})  # First(X) = { '', '+' }
    #     self._check_first(grammar, "Y", {'', '*'})  # First(Y) = { '', '*' }
    #     self._check_first(grammar, "", {''})  # First(ε) = { '' }
    #     self._check_first(grammar, "Y+i", {'+', '*'})  # First(Y+i) = { '+', '*' }
    #     self._check_first(grammar, "YX", {'+', '*', ''})  # First(YX) = { '+', '*', '' }
    #     self._check_first(grammar, "YXT", {'+', '*', 'i', '('})  # First(YXT) = { '+', '*', 'i', '(' }