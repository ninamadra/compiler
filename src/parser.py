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
        self.scope = 0
        self.label = 0

    # program_all productions

    @_('procedures main')
    def program_all(self, p):
        self.generator.readSymbolTable()
        if not p.procedures:
            return p.main
        return p.main + p.procedures

    # procedures productions

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        self.scope += 1
        return (
                p.proc_head[0] + " " +
                p.commands +
                self.generator.generateNumber(p.proc_head[1]) +
                self.generator.loadNumberFromAddress() +
                "INC a\n" +
                "INC a\n" +
                "INC a\n" +
                "JUMPR a\n" +
                p.procedures
        )

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        self.scope += 1
        return (
                p.proc_head[0] + " " +
                p.commands +
                self.generator.generateNumber(p.proc_head[1]) +
                self.generator.loadNumberFromAddress() +
                "INC a\n" +
                "INC a\n" +
                "INC a\n" +
                "JUMPR a\n" +
                p.procedures
        )

    @_('')
    def procedures(self, p):
        return ""

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
                self.__getLabel() + " "
        )

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return (
                p.condition +
                "JZERO " + self.__addLabel() + "\n" +
                p.commands +
                self.__getLabel() + " "
        )

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return (
                self.__addLabel() + " " +
                p.condition +
                "JZERO " + self.__getLabel(1) + "\n" +
                p.commands +
                "JUMP " + self.__getLabel() + "\n" +
                self.__addLabel() + " "
        )

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return (
                self.__addLabel() + " " +
                p.commands +
                p.condition +
                "JZERO " + self.__getLabel() + "\n"
        )

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

    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        procedure = self.generator.declareProcedure(
            p.PIDENTIFIER,
            self.__addLabel(),
            self.scope,
            p.args_decl,
        )
        return self.__getLabel(), procedure.returnAddress

    # proc_call productions

    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        procedure = self.generator.getProcedure(p.PIDENTIFIER)
        return (
                self.generator.assignArguments(procedure, p.args, self.scope) +
                self.generator.assignReturnAddress(procedure.returnAddress) +
                "JUMP " + procedure.line + "\n"
        )

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

    @_('args_decl COMMA PIDENTIFIER')
    def args_decl(self, p):
        self.generator.declareVariable(p.PIDENTIFIER, self.scope, True)
        return p.args_decl + [p.PIDENTIFIER]

    @_('args_decl COMMA T PIDENTIFIER')
    def args_decl(self, p):
        self.generator.declareArray(p.PIDENTIFIER, self.scope, 1, True)
        return p.args_decl + ["T " + p.PIDENTIFIER]

    @_('PIDENTIFIER')
    def args_decl(self, p):
        self.generator.declareVariable(p.PIDENTIFIER, self.scope, True)
        return [p.PIDENTIFIER]

    @_('T PIDENTIFIER')
    def args_decl(self, p):
        self.generator.declareArray(p.PIDENTIFIER, self.scope, 1, True)
        return ["T " + p.PIDENTIFIER]

    # args productions

    @_('args COMMA PIDENTIFIER')
    def args(self, p):
        return p.args + [p.PIDENTIFIER]

    @_('PIDENTIFIER')
    def args(self, p):
        return [p.PIDENTIFIER]

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
                self.__addLabel() + " RST f\n"
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
                "JUMP " + self.__getLabel(2) + "\n" +
                self.__addLabel() + " RST a\n" +
                self.__addLabel() + " "
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
                "RST a\n" +
                self.__addLabel() + " "
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
                "JPOS " + self.__getLabel(1) + "\n" +
                "INC a\n" +
                "JPOS " + self.__getLabel(2) + "\n" +
                self.__addLabel() + " RST a\n" +
                self.__addLabel() + " "

        )

    @_('value LESSEQUAL value')
    def condition(self, p):
        return (
                p.value1 +
                "PUT c\n" +
                p.value0 +
                "SUB c\n" +
                "JPOS " + self.__getLabel(1) + "\n" +
                "INC a\n" +
                "JPOS " + self.__getLabel(2) + "\n" +
                self.__addLabel() + " RST a\n" +
                self.__addLabel() + " "
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
        pid = self.generator.getVariable(p.PIDENTIFIER, self.scope)
        if not pid.isPointer:
            return self.generator.generateAddress(p.PIDENTIFIER, self.scope)
        return self.generator.generateAddressFromPointer(pid)

    @_('PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def identifier(self, p):
        pid = self.generator.getArray(p.PIDENTIFIER, self.scope)
        if not pid.isPointer:
            return self.generator.generateArrayElementAddress(p.PIDENTIFIER, p.NUMBER, self.scope)
        return self.generator.generateArrayElementAddressFromPointer(pid, p.NUMBER, self.scope)

    @_('PIDENTIFIER LBRACKET PIDENTIFIER RBRACKET')
    def identifier(self, p):
        pid0 = self.generator.getArray(p.PIDENTIFIER0, self.scope)
        pid1 = self.generator.getVariable(p.PIDENTIFIER1, self.scope)
        if not pid0.isPointer and not pid1.isPointer:
            return self.generator.generateArrayPidentifierElementAddress(p.PIDENTIFIER0, p.PIDENTIFIER1, self.scope)
        elif not pid0.isPointer and pid1.isPointer:
            return self.generator.generateArrayPidentifierElementPointerAddress(pid0, pid1)
        elif pid0.isPointer and not pid1.isPointer:
            return self.generator.generateArrayPidentifierPointerElementAddress(pid0, pid1)
        else:
            return self.generator.generateArrayPidentifierPointerElementPointerAddress(pid0, pid1)

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
