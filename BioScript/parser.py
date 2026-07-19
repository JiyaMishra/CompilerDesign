import ply.yacc as yacc

from lexer import tokens

# ----------------------------------------
# AST Node
# ----------------------------------------

class Node:
    def __init__(self, node_type, **kwargs):
        self.type = node_type
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"{self.type}({self.__dict__})"


# ----------------------------------------
# Program
# ----------------------------------------

def p_program(p):
    '''
    program : statements
    '''
    p[0] = p[1]


# ----------------------------------------
# Multiple Statements
# ----------------------------------------

def p_statements_multiple(p):
    '''
    statements : statements statement
    '''
    p[0] = p[1] + [p[2]]


def p_statements_single(p):
    '''
    statements : statement
    '''
    p[0] = [p[1]]


# ----------------------------------------
# Statements
# ----------------------------------------

def p_statement_sequence(p):
    '''
    statement : SEQUENCE IDENTIFIER ASSIGN STRING
    '''
    p[0] = Node(
        "sequence",
        name=p[2],
        value=p[4]
    )


def p_statement_transcribe(p):
    '''
    statement : TRANSCRIBE IDENTIFIER ARROW IDENTIFIER
    '''
    p[0] = Node(
        "transcribe",
        source=p[2],
        target=p[4]
    )


def p_statement_translate(p):
    '''
    statement : TRANSLATE IDENTIFIER ARROW IDENTIFIER
    '''
    p[0] = Node(
        "translate",
        source=p[2],
        target=p[4]
    )


def p_statement_reverse(p):
    '''
    statement : REVERSE IDENTIFIER ARROW IDENTIFIER
    '''
    p[0] = Node(
        "reverse",
        source=p[2],
        target=p[4]
    )


def p_statement_complement(p):
    '''
    statement : COMPLEMENT IDENTIFIER ARROW IDENTIFIER
    '''
    p[0] = Node(
        "complement",
        source=p[2],
        target=p[4]
    )


def p_statement_gc(p):
    '''
    statement : GC IDENTIFIER ARROW IDENTIFIER
    '''
    p[0] = Node(
        "gc",
        source=p[2],
        target=p[4]
    )


def p_statement_print(p):
    '''
    statement : PRINT IDENTIFIER
    '''
    p[0] = Node(
        "print",
        value=p[2]
    )


# ----------------------------------------
# Error Handling
# ----------------------------------------

def p_error(p):

    if p:
        print(f"Syntax error near '{p.value}'")

    else:
        print("Syntax error at EOF")


# ----------------------------------------
# Build Parser
# ----------------------------------------

parser = yacc.yacc()


# ----------------------------------------
# Test Parser
# ----------------------------------------

if __name__ == "__main__":

    code = '''

    sequence dna = "ATGCGTA"

    transcribe dna -> rna

    translate dna -> protein

    reverse dna -> rev

    complement dna -> comp

    gc dna -> gcvalue

    print protein

    '''

    ast = parser.parse(code)

    print()

    print("======= AST =======")

    for node in ast:
        print(node)