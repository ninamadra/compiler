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
        self.label = 0

    # program_all productions

    @_('procedures main')
    def program_all(self, p):
        if not p.procedures:
            return p.main
        return p.procedures + p.main

    # procedures productions

    # TODO
    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        return 'procedures'

    # TODO
    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        return 'procedures'

    # TODO
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
        return p.identifier + "PUT f\n" + p.expression + "STORE f\n"

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return (
            p.condition +
            "JZERO " + self.__addLabel() + "\n" +
            p.commands0 +
            "JUMP " + self.__addLabel() + "\n" +
            self.__getLabel(-1) + " " + p.commands1 +
            self.__getLabel() + " RST a\n"
        )

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return (
                p.condition +
                "JZERO " + self.__addLabel() + "\n" +
                p.commands +
                self.__getLabel() + " RST a\n"
        )

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return (
                self.__addLabel() + " RST a\n" +
                p.condition +
                "JZERO " + self.__getLabel(1) + "\n" +
                p.commands +
                self.__addLabel() + " JUMP " + self.__getLabel(-1) + "\n"
        )

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return (
            self.__addLabel() + " " +
            p.commands +
            p.condition +
            "JZERO " + self.__getLabel() + "\n"
        )

    # TODO
    @_('proc_call SEMICOLON')
    def command(self, p):
        return p.proc_call

    @_('READ identifier SEMICOLON')
    def command(self, p):
        return (
                p.identifier +
                "PUT b\n" +
                "READ\n" +
                "STORE b\n"
        )

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return p.value + "WRITE\n"

    # proc_head productions

    # TODO
    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        return ProcHeadNode(p.PIDENTIFIER, p.args_decl)

    # proc_call productions

    # TODO
    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        return ProcCallNode(p.PIDENTIFIER, p.args)

    # declarations productions

    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, p):
        self.generator.declareVariable(p.PIDENTIFIER, self.scope)
        return

    @_('declarations COMMA PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def declarations(self, p):
        self.generator.declareArray(p.PIDENTIFIER, self.scope, p.NUMBER)
        return

    @_('PIDENTIFIER')
    def declarations(self, p):
        self.generator.declareVariable(p.PIDENTIFIER, self.scope)
        return

    @_('PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def declarations(self, p):
        self.generator.declareArray(p.PIDENTIFIER, self.scope, p.NUMBER)
        return

    # args_decl productions

    # TODO
    @_('args_decl COMMA PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    # TODO
    @_('args_decl COMMA T PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    # TODO
    @_('PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    # TODO
    @_('T PIDENTIFIER')
    def args_decl(self, p):
        return p.PIDENTIFIER

    # args productions

    # TODO
    @_('args COMMA PIDENTIFIER')
    def args(self, p):
        return *p.args.args, p.PIDENTIFIER

    # TODO
    @_('PIDENTIFIER')
    def args(self, p):
        return p.PIDENTIFIER

    # expression productions

    @_('value')
    def expression(self, p):
        return p.value

    @_('value PLUS value')
    def expression(self, p):
        return p.value0 + "PUT c\n" + p.value1 + "ADD c\n"

    @_('value MINUS value')
    def expression(self, p):
        return (
                p.value0 +
                "PUT c\n" +
                p.value1 +
                "PUT d\n" +
                "GET c\n" +
                "SUB d\n"
        )

    @_('value TIMES value')
    def expression(self, p):
        return (
                p.value0 +
                "PUT d\n" +
                p.value1 +
                "RST e\n" +
                self.__addLabel() + " RST h\n"
                "JZERO " + self.__getLabel(2) + "\n" +
                "PUT b\n" +
                "PUT c\n" +
                "SHR b\n" +
                "SHL b\n" +
                "SUB b\n" +
                "JZERO " + self.__getLabel(1) + "\n" +
                "GET d\n" +
                "ADD e\n" +
                self.__addLabel() + " PUT e\n" +
                "SHL d\n" +
                "SHR c\n" +
                "GET c\n" +
                self.__addLabel() + " JUMP " + self.__getLabel(-2) + "\n" +
                "GET e\n"
        )

    # TODO
    @_('value DIVIDE value')
    def expression(self, p):
        return p.value0, p.value1

    # TODO
    @_('value MOD value')
    def expression(self, p):
        return p.value0, p.value1

    # condition productions

    @_('value EQUAL value')
    def condition(self, p):
        return (
            p.value0 +
            "PUT c\n" +
            p.value1 +
            "PUT b\n" +
            "SUB c\n" +
            "JPOS " + self.__getLabel(1) + "\n" +
            "GET c\n" +
            "SUB b\n" +
            "JPOS " + self.__getLabel(1) + "\n" +
            "INC a\n" +
            self.__addLabel() + " JUMP " + self.__getLabel(1) + "\n" +
            self.__addLabel() + " RST a\n"
        )

    @_('value NOTEQUAL value')
    def condition(self, p):
        return (
            p.value0 +
            "PUT c\n" +
            p.value1 +
            "PUT b\n" +
            "SUB c\n" +
            "JPOS " + self.__getLabel(1) + "\n" +
            "GET c\n" +
            "SUB b\n" +
            "JPOS " + self.__getLabel(1) + "\n" +
            self.__addLabel() + " RST a\n"
        )

    @_('value GREATER value')
    def condition(self, p):
        return (
                p.value1 +
                "PUT c\n" +
                p.value0 +
                "SUB c\n"
        )

    @_('value LESS value')
    def condition(self, p):
        return (
                p.value0 +
                "PUT c\n" +
                p.value1 +
                "SUB c\n"
        )

    @_('value GREATEREQUAL value')
    def condition(self, p):
        return (
                p.value0 +
                "PUT c\n" +
                p.value1 +
                "SUB c\n" +
                "JPOS " + self.__addLabel() + "\n" +
                "INC a\n" +
                self.__getLabel() + " JPOS " + self.__addLabel() + "\n" +
                self.__getLabel() + " RST a\n"
        )

    @_('value LESSEQUAL value')
    def condition(self, p):
        return (
                p.value1 +
                "PUT c\n" +
                p.value0 +
                "SUB c\n" +
                "JPOS " + self.__addLabel() + "\n" +
                "INC a\n" +
                self.__getLabel() + " JPOS " + self.__addLabel() + "\n" +
                self.__getLabel() + " RST a\n"
        )

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
        return self.generator.generateArrayPidentifierElementAddress(p.PIDENTIFIER0, p.PIDENTIFIER1, self.scope)

    # error production

    def error(self, p):
        if p:
            print(f"Syntax error near: {p.type}, {p.value}")
        else:
            print("Syntax error: Unexpected end of input")

    def __addLabel(self):
        self.label += 1
        return "label_" + str(self.label)

    def __getLabel(self, off=None):
        if off is None:
            return "label_" + str(self.label)
        else:
            return "label_" + str(self.label + off)

