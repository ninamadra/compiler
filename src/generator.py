from ast_node import *


class MyGenerator:
    def __init__(self):
        self.machine_code = []

    def generate(self, root):
        if isinstance(root, ProgramNode):
            self.generate_program(root)
        else:
            raise Exception(f"Unsupported node type: {type(root).__name__}")

    def generate_program(self, node):
        print("PROGRAM NODE")

        if node.procedures:
            self.generate_procedures(node.procedures)

        self.generate_main(node.main)

        self.machine_code.append("HALT")

    def generate_procedures(self, node):
        print("PROCEDURES NODE")

        for procedure in node.procedures:
            self.generate_procedure(procedure)

    def generate_procedure(self, node):
        print("PROCEDURE NODE")

        self.generate_proc_head(node.proc_head)
        self.generate_declaration(node.declarations)
        self.generate_commands(node.commands)

    def generate_main(self, node):
        print("MAIN NODE")

        self.generate_declarations(node.declarations)
        self.generate_commands(node.commands)

    def generate_commands(self, node):
        print("COMMANDS NODE")

        for command in node.commands:
            self.generate_command(command)

    def generate_command(self, command):
        if isinstance(command, AssignmentNode):
            self.generate_assignment(command)
        elif isinstance(command, IfNode):
            self.generate_if(command)
        elif isinstance(command, WhileNode):
            self.generate_while(command)
        elif isinstance(command, RepeatUntilNode):
            self.generate_repeat_until(command)
        elif isinstance(command, ReadNode):
            self.generate_read(command)
        elif isinstance(command, WriteNode):
            self.generate_write(command)
        elif isinstance(command, ProcCallNode):
            self.generate_proc_call(command)
        else:
            raise Exception(f"Unsupported command type: {type(command).__name__}")

    def generate_assignment(self, node):
        print("ASSIGNMENT NODE")

        self.generate_identifier(node.identifier)
        self.generate_expression(node.expression)

    def generate_if(self, node):
        print("IF NODE")

        self.generate_condition(node.condition)
        self.generate_commands(node.true_commands)
        if node.false_commands:
            print("ELSE")
            self.generate_commands(node.false_commands)
        print("ENDIF")

    def generate_while(self, node):
        print("WHILE NODE")

        self.generate_condition(node.condition)
        self.generate_commands(node.commands)
        print("ENDWHILE")

    def generate_repeat_until(self, node):
        print("REPEAT UNTIL NODE")

        self.generate_commands(node.commands)
        self.generate_condition(node.condition)
        print("ENDREPEAT")

    def generate_read(self, node):
        print("READ NODE")

        self.generate_identifier(node.identifier)

    def generate_write(self, node):
        print("WRITE NODE")

        self.generate_value(node.value)

    def generate_proc_head(self, node):
        print("PROC HEAD NODE")

        self.generate_args_decl(node.args_decl)

    def generate_proc_call(self, node):
        print("PROC CALL NODE")

        self.generate_args(node.args)

    def generate_declarations(self, node):
        print("DECLARATIONS NODE")

        for declaration in node.declarations:
            self.generate_declaration(declaration)

    def generate_declaration(self, node):
        print("DECLARATION NODE")

        if node.num is not None:
            print(f"Array Declaration: {node.PIDENTIFIER}[{node.num}]")
        else:
            print(f"Variable Declaration: {node.PIDENTIFIER}")

    def generate_args_decl(self, node):
        print("ARGS DECL NODE")

        for arg_decl in node.args_decl:
            self.generate_args_decl_item(arg_decl)

    def generate_args_decl_item(self, node):
        print("ARGS DECL ITEM NODE")

        if node.is_array:
            print(f"Array Argument: {node.PIDENTIFIER}")
        else:
            print(f"Variable Argument: {node.PIDENTIFIER}")

    def generate_args(self, node):
        print("ARGS NODE")

        for arg in node.args:
            self.generate_arg(arg)

    def generate_arg(self, node):
        print(f"ARG NODE: {node.PIDENTIFIER}")

    def generate_expression(self, node):
        print("EXPRESSION NODE")

        if isinstance(node, ExpressionNode):
            self.generate_value(node.left)
            print(f"Operator: {node.operator}")
            self.generate_value(node.right)
        else:
            self.generate_value(node)

    def generate_condition(self, node):
        print("CONDITION NODE")

        self.generate_value(node.left)
        print(f"Comparison Operator: {node.operator}")
        self.generate_value(node.right)

    def generate_value(self, node):
        print("VALUE NODE:")

        if isinstance(node, IdentifierNode):
            print(f"Identifier: {node.PIDENTIFIER}")
        else:
            print(f"Variable: {node}")

    def generate_identifier(self, node):
        print(f"IDENTIFIER NODE: {node.PIDENTIFIER}")

        if node.index is not None:
            print(f"Array Index: {node.index}")
