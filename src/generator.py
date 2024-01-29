from symboltable import SymbolTable


class MyGenerator:

    def __init__(self):
        self.symbols = SymbolTable()

    def getVariable(self, name, scope, line):
        var = self.symbols.getVariable(name, scope)
        arr = self.symbols.getArray(name, scope)
        if var is None:
            if arr is not None:
                raise Exception(f"Incorrect array '{name}' usage at line {line}.")
            raise Exception(f"Variable '{name}' not found, line: {line}.")
        return var

    def getArray(self, name, scope, line):
        arr = self.symbols.getArray(name, scope)
        var = self.symbols.getVariable(name, scope)
        if arr is None:
            if var is not None:
                raise Exception(f"Incorrect variable '{name}' usage at line {line}.")
            raise Exception(f"Array '{name}' not found, line: {line}.")
        return arr

    def getProcedure(self, name, line):
        return self.symbols.getProcedure(name, line)

    def declareVariable(self, name, scope, line, isPointer=False, isInitialized=False):
        return self.symbols.addVariable(name, scope, isPointer, line, isInitialized)

    def declareArray(self, name, scope, size, line, isPointer=False):
        return self.symbols.addArray(name, scope, int(size), isPointer, line)

    def declareProcedure(self, name, line, scope, args_decl, lineno, isDeclared=False):
        return self.symbols.addProcedure(name, line, scope, args_decl, lineno, isDeclared)

    def markVariableInitialized(self, name, scope):
        self.symbols.markVariableInitialized(name, scope)

    def markProceduresDeclared(self):
        self.symbols.markProceduresDeclared()

    @staticmethod
    def loadNumberFromAddress():
        return "PUT b\nLOAD b\n"

    @staticmethod
    def generateNumber(number):
        code = "RST a\n"
        binary_representation = bin(number)[2:]

        for bit in (binary_representation[:-1]):
            if bit == '1':
                code += "INC a\n"
            code += "SHL a\n"

        if binary_representation[-1] == '1':
            code += "INC a\n"

        return code

    def generateAddress(self, pidentifier, scope):
        variable = self.symbols.getVariable(pidentifier, scope)
        if variable is None:
            variable = self.symbols.getArray(pidentifier, scope)
        return self.generateNumber(int(variable.address))

    def generateAddressFromPointer(self, pid):
        code = self.generateNumber(int(pid.address))
        code += "LOAD a\n"
        return code

    def generateArrayElementAddress(self, pidentifier, number, scope):
        array = self.symbols.getArray(pidentifier, scope)
        return self.generateNumber(int(array.address) + int(number))

    def generateArrayElementAddressFromPointer(self, pid, number, scope):
        code = self.generateNumber(int(pid.address))
        code += "LOAD a\n"
        code += "PUT h\n"
        code += self.generateNumber(int(number))
        code += "ADD h\n"
        return code

    def generateArrayPidentifierElementAddress(self, pidentifier, index, scope):
        array = self.symbols.getArray(pidentifier, scope)
        index_variable = self.symbols.getVariable(index, scope)
        code = self.generateNumber(int(index_variable.address))
        code += self.loadNumberFromAddress()
        code += "PUT b\n"
        code += self.generateNumber(int(array.address))
        code += "ADD b\n"
        return code

    def generateArrayPidentifierPointerElementAddress(self, arr_pointer, index):
        code = self.generateNumber(int(index.address))
        code += "LOAD a\n"
        code += "PUT b\n"
        code += self.generateNumber(int(arr_pointer.address))
        code += "LOAD a\n"
        code += "ADD b\n"
        return code

    def generateArrayPidentifierElementPointerAddress(self, arr, index_pointer):
        code = self.generateNumber(int(index_pointer.address))
        code += "LOAD a\n"
        code += "LOAD a\n"
        code += "PUT b\n"
        code += self.generateNumber(int(arr.address))
        code += "ADD b\n"
        return code

    def generateArrayPidentifierPointerElementPointerAddress(self, arr_pointer, index_pointer):
        code = self.generateNumber(int(index_pointer.address))
        code += "LOAD a\n"
        code += "LOAD a\n"
        code += "PUT b\n"
        code += self.generateNumber(int(arr_pointer.address))
        code += "LOAD a\n"
        code += "ADD b\n"
        return code

    def assignReturnAddress(self, returnAddress):
        code = self.generateNumber(int(returnAddress))
        code += (
                "PUT b\n" +
                "STRK a\n" +
                "STORE b\n"
        )
        return code

    def assignArguments(self, procedure, arguments, scope, line):
        if len(arguments) != len(procedure.args_decl):
            raise Exception(f"Incorrect procedure call: {procedure.name}({arguments})")

        code = ""
        for arg, declaration in zip(arguments, procedure.args_decl):
            declared_arg = None
            real_arg = None
            if declaration.startswith('T'):
                declared_arg = self.symbols.getArray(declaration[2:], procedure.scope)
                if declared_arg is None:
                    raise Exception(
                        f"Argument T '{declaration[2:]}' not declared for procedure '{procedure.name}', line: {line}.")
                real_arg = self.symbols.getArray(arg, scope)
                real_arg2 = self.symbols.getVariable(arg, scope)
                if real_arg is None:
                    if real_arg2 is not None:
                        raise Exception(
                            f"Incorrect '{procedure.name}' procedure call with wrong argument usage for argument: '{arg}' at line {line}.")
                    raise Exception(
                        f"Argument T '{arg}' in procedure call {procedure.name}({arguments}) not found, line: {line}.")

            else:
                declared_arg = self.symbols.getVariable(declaration, procedure.scope)
                if declared_arg is None:
                    raise Exception(
                        f"Argument '{declaration[2:]}' not declared for procedure '{procedure.name}, line: {line}.")
                real_arg = self.symbols.getVariable(arg, scope)
                real_arg2 = self.symbols.getArray(arg, scope)
                if real_arg is None:
                    if real_arg2 is not None:
                        raise Exception(
                            f"Incorrect '{procedure.name}' procedure call with wrong argument usage for argument: '{arg}' at line {line}.")
                    raise Exception(
                        f"Argument '{arg}' in procedure call {procedure.name}({arguments}) not found, line: {line}.")

            code += self.generateNumber(int(declared_arg.address))
            code += "PUT h\n"
            code += self.generateNumber(int(real_arg.address))
            if real_arg.isPointer:
                code += "LOAD a\n"
            code += "STORE h\n"
        return code
