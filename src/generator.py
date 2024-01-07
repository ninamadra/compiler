from symboltable import SymbolTable


class MyGenerator:

    def __init__(self):
        self.symbols = SymbolTable()

    def readSymbolTable(self):
        return self.symbols.readSymbols()

    def declareVariable(self, name, scope, isPointer=False):
        return self.symbols.addVariable(name, scope, isPointer)

    def getVariable(self, name, scope):
        var = self.symbols.getVariable(name, scope)
        if var is None:
            raise Exception(f"Variable '{name}' not found in scope '{scope}'")
        return var

    def getArray(self, name, scope):
        arr = self.symbols.getArray(name, scope)
        if arr is None:
            raise Exception(f"Array '{name}' not found in scope '{scope}'")
        return arr

    def getProcedure(self, name):
        return self.symbols.getProcedure(name)

    def declareArray(self, name, scope, size, isPointer=False):
        return self.symbols.addArray(name, scope, int(size), isPointer)

    def declareProcedure(self, name, line, scope, args_decl):
        return self.symbols.addProcedure(name, line, scope, args_decl)

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
        code += "PUT c\n"
        code += self.generateNumber(int(number))
        code += "ADD c\n"
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
        code += "LOAD a\n"  # w a mamy wartosc indeksu
        code += "PUT b\n"
        code += self.generateNumber(int(arr_pointer.address)) # w a mamy arr_pointer
        code += "LOAD a\n"  # w a mamy adres arr
        code += "ADD b\n"
        return code

    def generateArrayPidentifierElementPointerAddress(self, arr, index_pointer):
        code = self.generateNumber(int(index_pointer.address))
        code += "LOAD a\n" # w a mamy adres indeksu
        code += "LOAD a\n" # w a mamy wartosc indeksu
        code += "PUT b\n"
        code += self.generateNumber(int(arr.address))
        code += "ADD b\n"
        return code

    def generateArrayPidentifierPointerElementPointerAddress(self, arr_pointer, index_pointer):
        code = self.generateNumber(int(index_pointer.address))
        code += "LOAD a\n"  # w a mamy adres indeksu
        code += "LOAD a\n"  # w a mamy wartosc indeksu
        code += "PUT b\n"
        code += self.generateNumber(int(arr_pointer.address))  # w a mamy arr_pointer
        code += "LOAD a\n"  # w a mamy adres arr
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

    def assignArguments(self, procedure, arguments, scope):
        if len(arguments) != len(procedure.args_decl):
            raise Exception(f"Incorrect procedure call: {procedure.name}({arguments})")

        code = ""
        for arg, declaration in zip(arguments, procedure.args_decl):
            declared_arg = None
            real_arg = None
            if declaration.startswith('T'):
                declared_arg = self.getArray(declaration[2:], procedure.scope)
                real_arg = self.getArray(arg, scope)
            else:
                declared_arg = self.getVariable(declaration, procedure.scope)
                real_arg = self.getVariable(arg, scope)
            code += self.generateNumber(int(declared_arg.address)) # w a mamy adres decl_arg
            code += "PUT h\n"
            code += self.generateNumber(int(real_arg.address)) # w a mamy adres arg a w h decl_arg
            code += "STORE h\n"
        return code
            # kod ktory pod adres declared_arg wstawi
            # real_arg.address jesli nie jest pointerem
            # i wartosc z adresu real_arg jesli jest




