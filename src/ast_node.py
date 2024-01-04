class ProgramNode:
    def __init__(self, procedures, main):
        self.procedures = procedures
        self.main = main


class ProceduresNode:
    def __init__(self, *procedures):
        self.procedures = list(procedures)


class ProcedureNode:
    def __init__(self, proc_head, declarations, commands):
        self.proc_head = proc_head
        self.declarations = declarations
        self.commands = commands


class MainNode:
    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands


class CommandsNode:
    def __init__(self, *commands):
        self.commands = list(commands)


class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression


class IfNode:
    def __init__(self, condition, true_commands, false_commands):
        self.condition = condition
        self.true_commands = true_commands
        self.false_commands = false_commands


class WhileNode:
    def __init__(self, condition, commands):
        self.condition = condition
        self.commands = commands


class RepeatUntilNode:
    def __init__(self, commands, condition):
        self.commands = commands
        self.condition = condition


class ReadNode:
    def __init__(self, identifier):
        self.identifier = identifier


class WriteNode:
    def __init__(self, value):
        self.value = value


class ProcHeadNode:
    def __init__(self, PIDENTIFIER, args_decl):
        self.PIDENTIFIER = PIDENTIFIER
        self.args_decl = args_decl


class ProcCallNode:
    def __init__(self, PIDENTIFIER, args):
        self.PIDENTIFIER = PIDENTIFIER
        self.args = args


class DeclarationsNode:
    def __init__(self, *declarations):
        self.declarations = list(declarations)


class DeclarationNode:
    def __init__(self, PIDENTIFIER, num=None):
        self.PIDENTIFIER = PIDENTIFIER
        self.num = num


class ArgsDeclNode:
    def __init__(self, *args_decl):
        self.args_decl = list(args_decl)


class ArgsDeclItemNode:
    def __init__(self, PIDENTIFIER, is_array=False):
        self.PIDENTIFIER = PIDENTIFIER
        self.is_array = is_array


class ArgsNode:
    def __init__(self, *args):
        self.args = list(args)


class ExpressionNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class ConditionNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class ValueNode:
    def __init__(self, value):
        self.value = value #NUM ALBO Identifier


class IdentifierNode:
    def __init__(self, PIDENTIFIER, index=None):
        self.PIDENTIFIER = PIDENTIFIER
        self.index = index
