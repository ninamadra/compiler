from sly import Parser
from lexer import MyLexer
from generator import MyGenerator


class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MOD),
    )

    def __init__(self):
        self.generator = MyGenerator()
        self.scope = ""

    # program_all productions

    @_('procedures main')
    def program_all(self, p):
        if not p.procedures:
            return p.main
        return p.procedures + p.main

    # procedures productions

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        return 'procedures'

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        return 'procedures'

    @_('')
    def procedures(self, p):
        return []

    # main productions

    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        return p.commands + "HALT\n"

    @_('PROGRAM IS IN commands END')
    def main(self, p):
        return p.commands + "HALT\n"

    # commands productions

    @_('commands command')
    def commands(self, p):
        return p.commands + p.command

    @_('command')
    def commands(self, p):
        return p.command

    # command productions

    @_("identifier ASSIGN expression SEMICOLON")
    def command(self, p):
        return AssignmentNode(p.identifier, p.expression)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return IfNode(p.condition, p.commands0, p.commands1)

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return IfNode(p.condition, p.commands, None)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return WhileNode(p.condition, p.commands)

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return RepeatUntilNode(p.commands, p.condition)

    @_('proc_call SEMICOLON')
    def command(self, p):
        return p.proc_call

    @_('READ identifier SEMICOLON')
    def command(self, p):
        code = p.identifier
        return code + "PUT b\nREAD\nSTORE b\n"

    @_('WRITE value SEMICOLON')
    def command(self, p):
        code = p.value
        return code + "WRITE\n"

    # proc_head productions

    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        return ProcHeadNode(p.PIDENTIFIER, p.args_decl)

    # proc_call productions

    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        return ProcCallNode(p.PIDENTIFIER, p.args)

    # declarations productions

    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, p):
        self.generator.declareVariable(p.PIDENTIFIER, self.scope)
        return p.declarations + [("VARIABLE", p.PIDENTIFIER)]

    @_('declarations COMMA PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def declarations(self, p):
        self.generator.declareArray(p.PIDENTIFIER, self.scope, p.NUMBER)
        return p.declarations + [("ARRAY", p.PIDENTIFIER, p.NUMBER)]

    @_('PIDENTIFIER')
    def declarations(self, p):
        self.generator.declareVariable(p.PIDENTIFIER, self.scope)
        return [("VARIABLE", p.PIDENTIFIER)]

    @_('PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def declarations(self, p):
        self.generator.declareArray(p.PIDENTIFIER, self.scope, p.NUMBER)
        return [("ARRAY", p.PIDENTIFIER, p.NUMBER)]

    # args_decl productions

    @_('args_decl COMMA PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    @_('args_decl COMMA T PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    @_('PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    @_('T PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    # args productions

    @_('args COMMA PIDENTIFIER')
    def args(self, p):
        return *p.args.args, p.PIDENTIFIER

    @_('PIDENTIFIER')
    def args(self, p):
        return p.PIDENTIFIER

    # expression productions

    @_('value',
       'value PLUS value',
       'value MINUS value',
       'value TIMES value',
       'value DIVIDE value',
       'value MOD value')
    def expression(self, p):
        if len(p) == 1:
            return p.value
        elif len(p) == 3:
            # kod maszynowy wykonuje operacje i wynik jest w A
            return p.value0, p.value1

    # condition productions

    @_('value EQUAL value',
       'value NOTEQUAL value',
       'value GREATER value',
       'value LESS value',
       'value GREATEREQUAL value',
       'value LESSEQUAL value')
    def condition(self, p):
        # jesli = : kod maszynowy ktory porowna i zaladuje 1 do akumulatora jesli prawda i 0 wpp
        # jesli != : kod maszynowy ktory porowna i zaladuje 1 do akumulatora jesli prawda i 0 wpp
        # jesli > : kod maszynowy ktory porowna i zaladuje 1 do akumulatora jesli prawda i 0 wpp
        # jesli < : kod maszynowy ktory porowna i zaladuje 1 do akumulatora jesli prawda i 0 wpp
        # jesli >= : kod maszynowy ktory porowna i zaladuje 1 do akumulatora jesli prawda i 0 wpp
        # jesli <- : kod maszynowy ktory porowna i zaladuje 1 do akumulatora jesli prawda i 0 wpp
        return

    # value productions

    @_('NUMBER')
    def value(self, p):
        return self.generator.generateNumber(int(p.NUMBER))

    @_('identifier')
    def value(self, p):
        return p.identifier + self.generator.loadNumberFromAddress()

    # identifier productions

    @_('PIDENTIFIER')
    def identifier(self, p):
        return self.generator.generateAddress(p.PIDENTIFIER, self.scope)

    @_('PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def identifier(self, p):
        return self.generator.generateArrayElementAddress(p.PIDENTIFIER, p.NUMBER, self.scope)

    @_('PIDENTIFIER LBRACKET PIDENTIFIER RBRACKET')
    def identifier(self, p):
        return self.generator.generateArrayPidentifierElementAddress(p[0], p[2], self.scope)

    # error production

    def error(self, p):
        if p:
            print(f"Syntax error near: {p.type}, {p.value}")
        else:
            print("Syntax error: Unexpected end of input")
