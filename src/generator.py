from symboltable import SymbolTable


class MyGenerator:

    def __init__(self):
        self.symbols = SymbolTable()

    def declareVariable(self, name, scope):
        self.symbols.addVariable(name, scope)

    def declareArray(self, name, scope, size):
        self.symbols.addArray(name, scope, int(size))

    def declareProcedure(self, name, line):
        self.symbols.addProcedure(name, line)

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
        return self.generateNumber(int(variable.address))

    def generateArrayElementAddress(self, pidentifier, number, scope):
        array = self.symbols.getArray(pidentifier, scope)
        return self.generateNumber(int(array.address) + int(number))

    def generateArrayPidentifierElementAddress(self, pidentifier, index, scope):
        array = self.symbols.getArray(pidentifier, scope)
        index_variable = self.symbols.getVariable(index, scope)
        code = self.generateNumber(int(index_variable.address))
        code += self.loadNumberFromAddress()
        code += "PUT b\n"
        code += self.generateNumber(int(array.address))
        code += "ADD b\n"
        return code
