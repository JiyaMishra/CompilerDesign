import ply.lex as lex


reserved = {
    'sequence': 'SEQUENCE',
    'transcribe': 'TRANSCRIBE',
    'translate': 'TRANSLATE',
    'reverse': 'REVERSE',
    'complement': 'COMPLEMENT',
    'gc': 'GC',
    'print': 'PRINT',
    'load': 'LOAD'
}


tokens = [
    'IDENTIFIER',
    'STRING',
    'ASSIGN',
    'ARROW'
] + list(reserved.values())


t_ASSIGN = r'='
t_ARROW = r'->'


t_ignore = ' \t'


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


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

    lexer.input(code)

    while True:
        tok = lexer.token()

        if not tok:
            break

        print(tok)