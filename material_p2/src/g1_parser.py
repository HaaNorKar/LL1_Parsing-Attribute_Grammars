import ply.yacc as yacc
from src.g1_lexer import tokens

# Grammar Rules for L = {a^n b^n c^k | k >= n + 1}
global errorflagG1
errorflagG1 = False

def p_Language(p):
    """
    Language : A B C
    """
    # Combine the attributes of A, B, and C
    nA = p[1]["nA"]  # Number of `a`s (from A)
    nB = p[2]["nB"]  # Number of `b`s (from B)
    k = p[3]["k"]  # Number of `c`s (from C)

    # Constraints
    if nA != nB or k < nA + 1 or errorflagG1 is True:
        p[0] = False
    else:
        p[0] = True


def p_A(p):
    """
    A : a A
      | lambda
    """
    if len(p) == 3:
        # Recursive case: A -> a A
        # Add 1 for the current `a` and propagate the count from the recursive call
        p[0] = {"nA": 1 + p[2]["nA"]}
    else:
        # Base case: A -> λ (empty production)
        # No `a`s to count, so return 0
        p[0] = {"nA": 0}


def p_B(p):
    """
    B : b B
      | lambda
    """
    if len(p) == 3:
        # Recursive case: B -> b B
        # Add 1 for the current `b` and propagate the count from the recursive call
        p[0] = {"nB": 1 + p[2]["nB"]}
    else:
        # Base case: B -> λ (empty production)
        # No `b`s to count, so return 0
        p[0] = {"nB": 0}


def p_C(p):
    """
    C : c C
      | c
    """
    if len(p) == 3:
        # Recursive case: C -> c C
        # Add 1 for the current `c` and propagate the count from the recursive call
        p[0] = {"k": 1 + p[2]["k"]}
    else:
        # Base case: C -> c (single `c`)
        # Count this single `c`, so return 1
        p[0] = {"k": 1}


def p_lambda(p):
    """
    lambda :
    """
    # Base case for an empty production
    # Both `n` (count of `a`s and `b`s) and `k` (count of `c`s) are 0
    p[0] = {"nA": 0, "nB" : 0, "k": 0}


# Syntax error handling
def p_error(p):
    # Set up global variable flag for syntax error
    errorflagG1 = True


# Construir el parser
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese una cadena: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es:", result)


