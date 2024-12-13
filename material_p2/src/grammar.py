from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )
        
        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom
        self.follow = {nt:None for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """
        firstElems: set[str] = set() # Set of first elements to be returned

        if sentence == '': # Special preventive case: if the sentence is void, it is always only started by lambda
            firstElems.add('')
            return firstElems
        
        for i in sentence: # Quick check, all elements in the string must be valid 
            if i not in self.terminals and i not in self.non_terminals:
                raise ValueError() # Error! invalid value in string

        voidFlag = True # Flag that indicates if lambda is a valid first element
        to_check = deque(sentence) # Queue of elements to check
        checked = set() # Set of checked elements to prevent endless looping

        while to_check and voidFlag is True: # Outer loop: run until lambda is not on the possible firsts or you reach end of chain
            voidFlag = False # Set it back to false
            current_char = to_check.popleft() # Get next element
            if current_char in self.terminals: # If the element is a terminal, add to list and carry on
                firstElems.add(current_char)
                break
            checked.add(current_char) # Otherwise add to checked elements and move on
            for case in self.productions[current_char]: # Loop through all possibilities of the first element
                if case == '': # If its lambda, set void to true
                    voidFlag = True
                elif case[0] in self.terminals: # Add to list if its terminal
                    firstElems.add(case[0])
                else: # Otherwise it's a non-terminal, add and explore
                    for i in case:
                        if i not in checked:
                            to_check.append(i)
                    voidFlag = True
        if voidFlag is True: # If the chain ends and lambda is still valid, add as posible first
            firstElems.add('')

        return firstElems
	


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """
        if symbol == '': # Special case: void strings cannot be worked with
            raise ValueError() # Error! Grammar cannot compute the follow of a void string
        
        for i in symbol: # Quick check that all elements are valid for this grammar
            if i not in self.terminals and i not in self.non_terminals:
                raise ValueError() # Error! invalid value in string

        if self.follow[symbol[-1]] is not None: # General case after determining the follows to avoid costly repetition of the operation
            return self.follow[symbol[-1]]  # Simply accesses the stored following symbols for the string
    
        # Otherwise, it's the first time they're being requested, and we go on to determine them
        followDict = {nt:set() for nt in self.non_terminals} # Dictionary of following symbols by nonterminal (we MUST do it like this to avoid infinite loops)
        followDict[self.axiom].add('$') # Adds the basic rule where the axiom is followed by the end of the chain
        changeflag = True

        while changeflag is True: # While there are changes being made compared to the last step, loop
            changeflag = False # Set the flag off
            for term in self.non_terminals: # First iterator: go over every grammatic non terminal element
                for key in self.productions: # Second iterator: run through all productions
                    prod_list = self.productions[key] # Get the content of the productions
                    if term != key: # Ignore the list of productions for that same term
                        for prod in prod_list: # Iterate over the productions for each key...
                            if term in prod: # Only if the term we're iterating for is in said production
                                position = prod.find(term) # Get the position of the term in the production
                                if position == len(prod)-1: # Case where term is at the end of the production
                                    if not followDict[term].issuperset(followDict[key]): # Only add and change if it has new elements (ie, is not superset)
                                        followDict[term].update(followDict[key]) # Assign as follow whatever follows the producer term
                                        changeflag = True # Set as true because changes were made. This applies for the two other rules below
                                else: # Case where it is followed by something else within the production
                                    addy = self.compute_first(prod[position+1]) # Get the set of first elements from the next term
                                    if '' in addy and position == len(prod)-2: # If that is the final term AND can be lambda...
                                        if not followDict[term].issuperset(followDict[key]):
                                            followDict[term].update(followDict[key]) # Then also add whatever follows the producer
                                            changeflag = True
                                    updated_elements = addy - {''}
                                    if not followDict[term].issuperset(updated_elements):
                                        followDict[term].update(updated_elements) # Add from the first elements
                                        changeflag = True

        
        self.follow = followDict # Assign the newly produced dictionary to avoid repeating this huge loop again and return it
        return followDict[symbol[-1]]
        
    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """
        firsts = {nt:self.compute_first(nt) for nt in self.non_terminals} # Set up a dictionary for the first elements
        ltable = LL1Table(self.non_terminals,self.terminals.union('$')) # Prepares the bones of the table with the elements

        for elem in self.non_terminals: # Outer loop: run through the elements to fill out the table
            for item in firsts[elem]: # First rule: For every first, put the production that matches it
                if item != '': # For the normal case where it isn't lambda
                    prods = self.productions[elem] # Get all productions
                    for i in prods: # Runs through every production for that non terminal
                        if item in self.compute_first(i): # Checks if the first element is a first for i
                            if ltable.cells[elem][item] == None: # Make sure the cell is empty
                                ltable.cells[elem][item] = i # Assigns the production to the empty cell
                            else: # There is no break to make sure no other production has the same first element
                                return None # If the cell isn't empty, there is ambiguity, and it isn't LL(1)!
                else: # The case where it is lambda: get the following elements and set those to lambda
                    for follow in self.compute_follow(elem): # Gets the set of following elements, should only compute once
                        if ltable.cells[elem][follow] == None: # Make sure the cell is empty
                            ltable.cells[elem][follow] = '' # Assigns lambda to the empty cell
                        else: # If the cell was already full, we do as in the other case
                            return None # If the cell isn't empty, there is ambiguity, and it isn't LL(1)!
        
        return ltable # If it managed to finish the table, there were no cases of ambiguity, and it is LL(1)


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell 

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )            
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        retTree = ParseTree(start) # Tree to be returned
        element_stack = deque([ParseTree("$"),retTree]) # Preps the stack that will be used in the loop
        input_chain = deque(input_string) # Turns input string into a stack to check as the code advances


        while element_stack and input_chain: # Primary loop: Run through the LL(1) table starting with the beginning symbol until it either ends or
                                             # an empty cell is accessed
            dad_tree = element_stack.pop() # Pops the right side, gets the next tree to expand
            stack_step = dad_tree.root # Gets the next stack element to check
            input_step = input_chain[0] # Gets the first element of the input string without popping it just yet
            if input_step not in self.terminals:
                raise SyntaxError() # Syntax error! This is not a valid character
            if stack_step in self.terminals: # First check if the current top of the pile is a terminal, and if it's accepted
                if stack_step != input_step:
                    raise SyntaxError() # Syntax error! Input char is not correct
                else:
                    input_chain.popleft() # Simply pops the input and continues, without creating a new tree child
            else:
                cell_value = self.cells[stack_step][input_step] # Value of the table cell for this step
                if cell_value is None: # Second, make sure there is a not None value for the table's cell
                    raise SyntaxError() # Syntax error! No valid table value for this terminal
                else:
                    children = list() # Children for the current dad tree
                    for char in cell_value[::-1]: # Go through the new stack chars in reverse order
                        newTree = ParseTree(char) # Make a new tree
                        element_stack.append(newTree) # Append (add to the right) the new tree
                        children.insert(0,newTree) # Add new tree to children
                    if not children: # Adds empty node to any non-terminals that would otherwise become leaves
                        children.insert(0,ParseTree(""))
                    dad_tree.add_children(children) # Add the children as collection of ParseTrees
        if element_stack or input_chain: # If the input ends improperly, raise syntax error
            raise SyntaxError()
        return retTree # At the end, return the top of the tree
  
class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
