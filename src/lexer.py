from sly import Lexer


class MyLexer(Lexer):
    tokens = {
        PROGRAM, PROCEDURE, IS, IN, END, SEMICOLON, NUMBER, ASSIGN, IF,
        THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE, REPEAT, UNTIL, READ, WRITE,
        COMMA, LPAREN, RPAREN, LBRACKET, RBRACKET, PLUS, MINUS, TIMES, DIVIDE,
        MOD, EQUAL, NOTEQUAL, GREATER, LESS, GREATEREQUAL, LESSEQUAL, T, PIDENTIFIER
    }

    ignore = ' \t'

    PROGRAM = r'PROGRAM'
    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    IN = r'IN'

    ENDWHILE = r'ENDWHILE'
    ENDIF = r'ENDIF'
    END = r'END'

    SEMICOLON = r';'
    COMMA = r','
    ASSIGN = r':='

    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'

    WHILE = r'WHILE'
    DO = r'DO'

    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'

    READ = r'READ'
    WRITE = r'WRITE'

    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'

    NOTEQUAL = r'!='
    GREATEREQUAL = r'>='
    LESSEQUAL = r'<='
    EQUAL = r'='

    GREATER = r'>'
    LESS = r'<'

    T = r'T'

    PIDENTIFIER = r'[_a-z]+'
    NUMBER = r'\d+'

    @_(r'#.*')
    def COMMENT(self, t):
        self.ignore

    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1
