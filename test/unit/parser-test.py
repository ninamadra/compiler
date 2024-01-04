import unittest
from lexer import MyLexer
from parser import MyParser
from ast_node import *


class TestMyParser(unittest.TestCase):
    def setUp(self):
        self.lexer = MyLexer()
        self.parser = MyParser()

    def parse(self, code):
        tokens = self.lexer.tokenize(code)
        result = self.parser.parse(tokens)
        return result

    def test_simple_program(self):
        code = """
        PROGRAM IS
        IN
            a := 42;
        END
        """
        result = self.parse(code)

        # Assertions for the parse tree structure
        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertEqual(len(result.main.commands.commands), 1)

        # Assertions for the assignment statement
        assignment_node = result.main.commands.commands[0]
        self.assertIsInstance(assignment_node, AssignmentNode)
        self.assertEqual(assignment_node.identifier.PIDENTIFIER, 'a')
        self.assertEqual(assignment_node.expression, '42')

    def test_multiple_commands(self):
        code = """
                PROGRAM IS
                IN
                    a := 42;
                    b := 123;
                    a := a + b;
                    WRITE a;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 4)

    def test_with_declarations(self):
        code = """
                PROGRAM IS
                n, p
                IN
                    READ n;
                    p:=n;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.declarations, DeclarationsNode)
        self.assertEqual(len(result.main.declarations.declarations), 2)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 2)

    def test_program_with_array_and_procedure(self):
        code = """
                PROGRAM IS
                n, arr[100]
                IN
                    n := 99;
                    arr[1] := n;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.declarations, DeclarationsNode)
        self.assertEqual(len(result.main.declarations.declarations), 2)

        # Check the first declaration (n)
        first_declaration = result.main.declarations.declarations[0]
        self.assertIsInstance(first_declaration, DeclarationNode)
        self.assertEqual(first_declaration.PIDENTIFIER, 'n')
        self.assertIsNone(first_declaration.num)

        # Check the second declaration (arr[100])
        second_declaration = result.main.declarations.declarations[1]
        self.assertIsInstance(second_declaration, DeclarationNode)
        self.assertEqual(second_declaration.PIDENTIFIER, 'arr')
        self.assertEqual(second_declaration.num, '100')

        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 2)

        # Check the first command (n := 99)
        first_command = result.main.commands.commands[0]
        self.assertIsInstance(first_command, AssignmentNode)
        self.assertIsInstance(first_command.identifier, IdentifierNode)
        self.assertEqual(first_command.identifier.PIDENTIFIER, 'n')
        self.assertEqual(first_command.expression, '99')

        # Check the second command (arr[1] := n)
        second_command = result.main.commands.commands[1]
        self.assertIsInstance(second_command, AssignmentNode)
        self.assertIsInstance(second_command.identifier, IdentifierNode)
        self.assertEqual(second_command.identifier.PIDENTIFIER, 'arr')
        self.assertEqual(second_command.identifier.index, '1')
        self.assertIsInstance(second_command.expression, IdentifierNode)
        self.assertEqual(second_command.expression.PIDENTIFIER, 'n')

    def test_program_with_loop(self):
        code = """
                PROGRAM IS
                IN
                    a := 5;
                    WHILE a > 0 DO
                        WRITE a;
                        a := a - 1;
                    ENDWHILE
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 2)

        # Check the first command (a := 5)
        first_command = result.main.commands.commands[0]
        self.assertIsInstance(first_command, AssignmentNode)
        self.assertIsInstance(first_command.identifier, IdentifierNode)
        self.assertEqual(first_command.identifier.PIDENTIFIER, 'a')
        self.assertEqual(first_command.expression, '5')

        # Check the second command (while loop)
        second_command = result.main.commands.commands[1]
        self.assertIsInstance(second_command, WhileNode)
        self.assertIsInstance(second_command.condition, ConditionNode)
        self.assertIsInstance(second_command.condition.left, IdentifierNode)
        self.assertEqual(second_command.condition.left.PIDENTIFIER, 'a')
        self.assertEqual(second_command.condition.operator, '>')
        self.assertEqual(second_command.condition.right, '0')

        # Check the third command inside the loop (WRITE a)
        third_command_inside_loop = second_command.commands.commands[0]
        self.assertIsInstance(third_command_inside_loop, WriteNode)
        self.assertIsInstance(third_command_inside_loop.value, IdentifierNode)
        self.assertEqual(third_command_inside_loop.value.PIDENTIFIER, 'a')

        # Check the fourth command inside the loop (a := a - 1)
        fourth_command_inside_loop = second_command.commands.commands[1]
        self.assertIsInstance(fourth_command_inside_loop, AssignmentNode)
        self.assertIsInstance(fourth_command_inside_loop.identifier, IdentifierNode)
        self.assertEqual(fourth_command_inside_loop.identifier.PIDENTIFIER, 'a')
        self.assertIsInstance(fourth_command_inside_loop.expression, ExpressionNode)
        self.assertEqual(fourth_command_inside_loop.expression.operator, '-')
        self.assertIsInstance(fourth_command_inside_loop.expression.left, IdentifierNode)
        self.assertEqual(fourth_command_inside_loop.expression.left.PIDENTIFIER, 'a')
        self.assertEqual(fourth_command_inside_loop.expression.right, '1')

    def test_if_else_statement(self):
        code = """
                PROGRAM IS
                IN
                    a := 10;
                    b := 5;
                    IF a > b THEN
                        WRITE a;
                    ELSE
                        WRITE b;
                    ENDIF
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 3)

        # Check the first command (a := 10)
        first_command = result.main.commands.commands[0]
        self.assertIsInstance(first_command, AssignmentNode)
        self.assertIsInstance(first_command.identifier, IdentifierNode)
        self.assertEqual(first_command.identifier.PIDENTIFIER, 'a')
        self.assertEqual(first_command.expression, '10')

        # Check the second command (b := 5)
        second_command = result.main.commands.commands[1]
        self.assertIsInstance(second_command, AssignmentNode)
        self.assertIsInstance(second_command.identifier, IdentifierNode)
        self.assertEqual(second_command.identifier.PIDENTIFIER, 'b')
        self.assertEqual(second_command.expression,'5')

        # Check the third command (IF ELSE statement)
        if_else_statement = result.main.commands.commands[2]
        self.assertIsInstance(if_else_statement, IfNode)
        self.assertIsInstance(if_else_statement.condition, ConditionNode)
        self.assertIsInstance(if_else_statement.condition.left, IdentifierNode)
        self.assertEqual(if_else_statement.condition.left.PIDENTIFIER, 'a')
        self.assertEqual(if_else_statement.condition.operator, '>')
        self.assertIsInstance(if_else_statement.condition.right, IdentifierNode)
        self.assertEqual(if_else_statement.condition.right.PIDENTIFIER, 'b')

        # Check the true_commands inside IF
        true_commands = if_else_statement.true_commands
        self.assertIsInstance(true_commands, CommandsNode)
        self.assertEqual(len(true_commands.commands), 1)
        write_command_inside_if = true_commands.commands[0]
        self.assertIsInstance(write_command_inside_if, WriteNode)
        self.assertIsInstance(write_command_inside_if.value, IdentifierNode)
        self.assertEqual(write_command_inside_if.value.PIDENTIFIER, 'a')

        # Check the false_commands inside ELSE
        false_commands = if_else_statement.false_commands
        self.assertIsInstance(false_commands, CommandsNode)
        self.assertEqual(len(false_commands.commands), 1)
        write_command_inside_else = false_commands.commands[0]
        self.assertIsInstance(write_command_inside_else, WriteNode)
        self.assertIsInstance(write_command_inside_else.value, IdentifierNode)
        self.assertEqual(write_command_inside_else.value.PIDENTIFIER, 'b')

    def test_repeat_until(self):
        code = """
                PROGRAM IS
                IN
                    a := 0;
                    REPEAT
                        a := a + 1;
                    UNTIL a = 5;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 2)

        # Check the first command (a := 0)
        first_command = result.main.commands.commands[0]
        self.assertIsInstance(first_command, AssignmentNode)
        self.assertIsInstance(first_command.identifier, IdentifierNode)
        self.assertEqual(first_command.identifier.PIDENTIFIER, 'a')
        self.assertEqual(first_command.expression, '0')

        # Check the second command (REPEAT UNTIL)
        repeat_until_command = result.main.commands.commands[1]
        self.assertIsInstance(repeat_until_command, RepeatUntilNode)
        self.assertIsInstance(repeat_until_command.commands, CommandsNode)
        self.assertEqual(len(repeat_until_command.commands.commands), 1)

        # Check the command inside the loop (a := a + 1)
        command_inside_loop = repeat_until_command.commands.commands[0]
        self.assertIsInstance(command_inside_loop, AssignmentNode)
        self.assertIsInstance(command_inside_loop.identifier, IdentifierNode)
        self.assertEqual(command_inside_loop.identifier.PIDENTIFIER, 'a')
        self.assertIsInstance(command_inside_loop.expression, ExpressionNode)
        self.assertEqual(command_inside_loop.expression.operator, '+')
        self.assertIsInstance(command_inside_loop.expression.left, IdentifierNode)
        self.assertEqual(command_inside_loop.expression.left.PIDENTIFIER, 'a')
        self.assertEqual(command_inside_loop.expression.right, '1')

        # Check the condition (UNTIL a = 5)
        repeat_until_condition = repeat_until_command.condition
        self.assertIsInstance(repeat_until_condition, ConditionNode)
        self.assertIsInstance(repeat_until_condition.left, IdentifierNode)
        self.assertEqual(repeat_until_condition.left.PIDENTIFIER, 'a')
        self.assertEqual(repeat_until_condition.operator, '=')
        self.assertEqual(repeat_until_condition.right, '5')

    def test_expressions(self):
        code = """
                PROGRAM IS
                IN
                    a := 5;
                    b := 3;
                    c := a + b;
                    d := a - b;
                    e := a * b;
                    f := a / b;
                    g := a % b;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 7)

        # Check addition (c := a + b)
        addition_command = result.main.commands.commands[2]
        self.assertIsInstance(addition_command, AssignmentNode)
        self.assertIsInstance(addition_command.expression, ExpressionNode)
        self.assertEqual(addition_command.expression.operator, '+')

        # Check subtraction (d := a - b)
        subtraction_command = result.main.commands.commands[3]
        self.assertIsInstance(subtraction_command, AssignmentNode)
        self.assertIsInstance(subtraction_command.expression, ExpressionNode)
        self.assertEqual(subtraction_command.expression.operator, '-')

        # Check multiplication (e := a * b)
        multiplication_command = result.main.commands.commands[4]
        self.assertIsInstance(multiplication_command, AssignmentNode)
        self.assertIsInstance(multiplication_command.expression, ExpressionNode)
        self.assertEqual(multiplication_command.expression.operator, '*')

        # Check division (f := a / b)
        division_command = result.main.commands.commands[5]
        self.assertIsInstance(division_command, AssignmentNode)
        self.assertIsInstance(division_command.expression, ExpressionNode)
        self.assertEqual(division_command.expression.operator, '/')

        # Check modulus (g := a % b)
        modulus_command = result.main.commands.commands[6]
        self.assertIsInstance(modulus_command, AssignmentNode)
        self.assertIsInstance(modulus_command.expression, ExpressionNode)
        self.assertEqual(modulus_command.expression.operator, '%')

    def test_program_with_one_procedure(self):
        code = """
                PROCEDURE square(x) IS
                x
                IN
                    x := x * x;
                    WRITE x;
                END

                PROGRAM IS
                a
                IN
                    a := 5;
                    square(a);
                    WRITE a;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)

        # Check the procedures
        self.assertIsInstance(result.procedures, ProceduresNode)
        self.assertEqual(len(result.procedures.procedures), 1)

        # Check the procedure (square)
        square_procedure = result.procedures.procedures[0]
        self.assertIsInstance(square_procedure, ProcedureNode)
        self.assertIsInstance(square_procedure.proc_head, ProcHeadNode)
        self.assertEqual(square_procedure.proc_head.PIDENTIFIER, 'square')
        self.assertIsInstance(square_procedure.declarations, DeclarationsNode)
        self.assertEqual(len(square_procedure.declarations.declarations), 1)
        self.assertIsInstance(square_procedure.commands, CommandsNode)
        self.assertEqual(len(square_procedure.commands.commands), 2)

        # Check the main block
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.declarations, DeclarationsNode)
        self.assertEqual(len(result.main.declarations.declarations), 1)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 3)

    def test_program_with_two_procedures(self):
        code = """
                PROCEDURE double(x) IS
                x
                IN
                    x := x * 2;
                END

                PROCEDURE square(y) IS
                y
                IN
                    y := y * y;
                END

                PROGRAM IS
                a, b
                IN
                    a := 5;
                    double(a);
                    square(a);
                    b := a * 3;
                    WRITE b;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)

        # Check the procedures
        self.assertIsInstance(result.procedures, ProceduresNode)
        self.assertEqual(len(result.procedures.procedures), 2)

        # Check the first procedure (double)
        double_procedure = result.procedures.procedures[0]
        self.assertIsInstance(double_procedure, ProcedureNode)
        self.assertIsInstance(double_procedure.proc_head, ProcHeadNode)
        self.assertEqual(double_procedure.proc_head.PIDENTIFIER, 'double')
        self.assertIsInstance(double_procedure.declarations, DeclarationsNode)
        self.assertEqual(len(double_procedure.declarations.declarations), 1)
        self.assertIsInstance(double_procedure.commands, CommandsNode)
        self.assertEqual(len(double_procedure.commands.commands), 1)

        # Check the second procedure (square)
        square_procedure = result.procedures.procedures[1]
        self.assertIsInstance(square_procedure, ProcedureNode)
        self.assertIsInstance(square_procedure.proc_head, ProcHeadNode)
        self.assertEqual(square_procedure.proc_head.PIDENTIFIER, 'square')
        self.assertIsInstance(square_procedure.declarations, DeclarationsNode)
        self.assertEqual(len(square_procedure.declarations.declarations), 1)
        self.assertIsInstance(square_procedure.commands, CommandsNode)
        self.assertEqual(len(square_procedure.commands.commands), 1)

        # Check the main block
        self.assertIsInstance(result.main, MainNode)
        self.assertIsInstance(result.main.declarations, DeclarationsNode)
        self.assertEqual(len(result.main.declarations.declarations), 2)
        self.assertIsInstance(result.main.commands, CommandsNode)
        self.assertEqual(len(result.main.commands.commands), 5)

    def test_procedure_calls(self):
        code = """
                PROCEDURE double(x) IS
                x
                IN
                    x := x * 2;
                END

                PROCEDURE square(y) IS
                y
                IN
                    y := y * y;
                END

                PROGRAM IS
                a, b
                IN
                    a := 5;
                    double(a);
                    square(a);
                    b := a * 3;
                    WRITE b;
                END
                """
        result = self.parse(code)

        self.assertIsInstance(result, ProgramNode)

        # Check the procedures
        self.assertIsInstance(result.procedures, ProceduresNode)
        self.assertEqual(len(result.procedures.procedures), 2)

        # Check the first procedure call (double)
        first_call = result.main.commands.commands[1]
        self.assertIsInstance(first_call, ProcCallNode)
        self.assertEqual(first_call.PIDENTIFIER, 'double')
        self.assertIsInstance(first_call.args, ArgsNode)
        self.assertEqual(len(first_call.args.args), 1)
        self.assertEqual(first_call.args.args[0], 'a')

        # Check the second procedure call (square)
        second_call = result.main.commands.commands[2]
        self.assertIsInstance(second_call, ProcCallNode)
        self.assertEqual(second_call.PIDENTIFIER, 'square')
        self.assertIsInstance(second_call.args, ArgsNode)
        self.assertEqual(len(second_call.args.args), 1)
        self.assertEqual(second_call.args.args[0], 'a')


if __name__ == '__main__':
    unittest.main()
