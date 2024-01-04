from sly import Parser
from lexer import MyLexer
from ast_node import *


class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MOD),
    )

    # program_all productions

    @_('procedures main')
    def program_all(self, p):
        return ProgramNode(p.procedures, p.main)

    # procedures productions

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        return ProceduresNode(*p.procedures.procedures, ProcedureNode(p.proc_head, p.declarations, p.commands))

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        return ProceduresNode(*p.procedures.procedures, ProcedureNode(p.proc_head, None, p.commands))

    @_('')
    def procedures(self, p):
        return ProceduresNode()

    # main productions

    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        return MainNode(p.declarations, p.commands)

    @_('PROGRAM IS IN commands END')
    def main(self, p):
        return MainNode(None, p.commands)

    # commands productions

    @_('commands command')
    def commands(self, p):
        return CommandsNode(*p.commands.commands, p.command)

    @_('command')
    def commands(self, p):
        return CommandsNode(p.command)

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
        return ReadNode(p.identifier)

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return WriteNode(p.value)

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
        return DeclarationsNode(*p.declarations.declarations, DeclarationNode(p.PIDENTIFIER))

    @_('declarations COMMA PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def declarations(self, p):
        return DeclarationsNode(*p.declarations.declarations, DeclarationNode(p.PIDENTIFIER, p.NUMBER))

    @_('PIDENTIFIER')
    def declarations(self, p):
        return DeclarationsNode(DeclarationNode(p.PIDENTIFIER))

    @_('PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def declarations(self, p):
        return DeclarationsNode(DeclarationNode(p.PIDENTIFIER, p.NUMBER))

    # args_decl productions

    @_('args_decl COMMA PIDENTIFIER')
    def args_decl(self, p):
        return ArgsDeclNode(*p.args_decl.args_decl, ArgsDeclItemNode(p.PIDENTIFIER))

    @_('args_decl COMMA T PIDENTIFIER')
    def args_decl(self, p):
        return ArgsDeclNode(*p.args_decl.args_decl, ArgsDeclItemNode(p.PIDENTIFIER, True))

    @_('PIDENTIFIER')
    def args_decl(self, p):
        return ArgsDeclNode(ArgsDeclItemNode(p.PIDENTIFIER))

    @_('T PIDENTIFIER')
    def args_decl(self, p):
        return ArgsDeclNode(ArgsDeclItemNode(p.PIDENTIFIER, True))

    # args productions

    @_('args COMMA PIDENTIFIER')
    def args(self, p):
        return ArgsNode(*p.args.args, p.PIDENTIFIER)

    @_('PIDENTIFIER')
    def args(self, p):
        return ArgsNode(p.PIDENTIFIER)

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
            return ExpressionNode(p.value0, p[1], p.value1)

    # condition productions

    @_('value EQUAL value',
       'value NOTEQUAL value',
       'value GREATER value',
       'value LESS value',
       'value GREATEREQUAL value',
       'value LESSEQUAL value')
    def condition(self, p):
        return ConditionNode(p.value0, p[1], p.value1)

    # value productions

    @_('NUMBER')
    def value(self, p):
        return p.NUMBER

    @_('identifier')
    def value(self, p):
        return p.identifier

    # identifier productions

    @_('PIDENTIFIER')
    def identifier(self, p):
        return IdentifierNode(p.PIDENTIFIER)

    @_('PIDENTIFIER LBRACKET NUMBER RBRACKET')
    def identifier(self, p):
        return IdentifierNode(p.PIDENTIFIER, p.NUMBER)

    @_('PIDENTIFIER LBRACKET PIDENTIFIER RBRACKET')
    def identifier(self, p):
        return IdentifierNode(p.PIDENTIFIER, p[2])

    # error production

    def error(self, p):
        if p:
            print(f"Syntax error near: {p.type}, {p.value}")
        else:
            print("Syntax error: Unexpected end of input")
