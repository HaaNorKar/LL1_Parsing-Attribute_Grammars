import ply.yacc as yacc
from src.roman_lexer import tokens

# Gramática
global errorflagRoman 
errorflagRoman = False

def p_romanNumber(p):
    """
    Language : Hundred Tens Units
    """

    global errorflagRoman
    # Get count
    countH = p[1]["count"]
    countT = p[2]["count"]
    countU = p[3]["count"]

    # Constraints
    if countH > 3 or countT > 3 or countU > 3 or errorflagRoman is True:
        p[0] = {"val":-1, "valid":False}
        errorflagRoman = False # Resets the global variable for the next test in case it was changed
        return

    # If valid, calculate arabic number and return in dictionary
    value = p[1]["value"]+p[2]["value"]+p[3]["value"]
    p[0] = {"val":value, "valid":True}



def p_small_hundred(p):
    """
    LowHundreds : C LowHundreds
                | lambda
    """
    if len(p) == 3:
        p[0] = {"count": 1 + p[2]["count"], "value": 100 + p[2]["value"]}
    else:
        p[0] = {"count": 0, "value": 0}


def p_hundred(p):
    """
    Hundred : LowHundreds
            | C D
            | D LowHundreds
            | C M
    """
    if len(p) == 2:
        p[0] = {"count": p[1]["count"], "value": p[1]["value"]}
    elif p[2] == 'D':
        p[0] = {"count": 0, "value": 400}
    elif p[2] == 'M':
        p[0] = {"count": 0, "value": 900}
    else:
        p[0] = {"count": p[2]["count"], "value": 500+p[2]["value"]}

def p_small_ten(p):
    """
    LowTens : X LowTens 
            | lambda
    """
    if len(p) == 3:
        p[0] = {"count": 1 + p[2]["count"], "value": 10 + p[2]["value"]}
    else:
        p[0] = {"count": 0, "value": 0}

def p_ten(p):
    """
    Tens : LowTens
         | X L
         | L LowTens
         | X C
    """
    if len(p) == 2:
        p[0] = {"count": p[1]["count"], "value": p[1]["value"]}
    elif p[2] == 'L':
        p[0] = {"count": 0, "value": 40}
    elif p[2] == 'C':
        p[0] = {"count": 0, "value": 90}
    else:
        p[0] = {"count": p[2]["count"], "value": 50+p[2]["value"]}


def p_small_digit(p):
    """
    LowUnits : I LowUnits 
             | lambda
    """
    if len(p) == 3:
        p[0] = {"count": 1 + p[2]["count"], "value": 1 + p[2]["value"]}
    else:
        p[0] = {"count": 0, "value": 0}

def p_digit(p):
    """
    Units : LowUnits
          | I V
          | V LowUnits
          | I X
    """
    if len(p) == 2:
        p[0] = {"count": p[1]["count"], "value": p[1]["value"]}
    elif p[2] == 'V':
        p[0] = {"count": 0, "value": 4}
    elif p[2] == 'X':
        p[0] = {"count": 0, "value": 9}
    else:
        p[0] = {"count": p[2]["count"], "value": 5+p[2]["value"]}


# Definir lambda
def p_empty(p):
    'lambda :'
    pass


# Manejo de errores sintácticos
def p_error(p):
    global errorflagRoman
    errorflagRoman = True

# Construir el parser
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese un número romano: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es: {result}")

