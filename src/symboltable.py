class SymbolTable:

    def __init__(self):
        self.variables = []
        self.arrays = []
        self.procedures = []
        self.mem_current = 0

    def addVariable(self, name, scope, isPointer=False):
        self.checkRedeclaration(name, scope)
        variable = Variable(name, self.assignAddress(1), scope, isPointer)
        self.variables.append(variable)
        return variable

    def addArray(self, name, scope, size, isPointer=False):
        self.checkRedeclaration(name, scope)
        array = Array(name, self.assignAddress(size), scope, size, isPointer)
        self.arrays.append(array)
        return array

    def addProcedure(self, name, line, scope, args_decl):
        for procedure in self.procedures:
            if procedure.name == name:
                raise Exception(f"Procedure {name} already exists")
        procedure = Procedure(name, line, scope, args_decl, self.addVariable("r_" + name, scope).address)
        self.procedures.append(procedure)
        return procedure

    def checkRedeclaration(self, name, scope):
        for var in self.variables:
            if var.name == name and var.scope == scope:
                raise Exception(f"Variable {name} already declared in scope {scope}")
        for arr in self.arrays:
            if arr.name == name and arr.scope == scope:
                raise Exception(f"Array {name} already declared in scope {scope}")

    def assignAddress(self, size):
        address = self.mem_current
        self.mem_current += size
        return address

    def getVariable(self, name, scope):
        for variable in self.variables:
            if variable.name == name and variable.scope == scope:
                return variable
        return None

    def getArray(self, name, scope):
        for array in self.arrays:
            if array.name == name and array.scope == scope:
                return array
        return None

    def getProcedure(self, name):
        for procedure in self.procedures:
            if procedure.name == name:
                return procedure
        return Exception(f"Procedure '{name}' does not exist'")

    def readSymbols(self):
        print("variables")
        for var in self.variables:
            print("name: ", var.name, " address: ", var.address, " scope: ", var.scope, " isPointer: ", var.isPointer)
        print("arrays")
        for var in self.arrays:
            print("name: ", var.name, " address: ", var.address, " scope: ", var.scope, " size: ", var.size, " isPointer: ", var.isPointer)
        print("procedures")
        for procedure in self.procedures:
            print("name: ", procedure.name, " label: ", procedure.line, "args_decl: ", str(procedure.args_decl), "return adress: ", procedure.returnAddress)


class Variable:
    def __init__(self, name, address, scope, isPointer=False, isInitialized=False):
        self.name = name
        self.address = address
        self.scope = scope
        self.isPointer = isPointer


class Array:
    def __init__(self, name, address, scope, size, isPointer=False):
        self.name = name
        self.address = address
        self.scope = scope
        self.size = size
        self.isPointer = isPointer


class Procedure:
    def __init__(self, name, line, scope, args_decl, returnAddress=0):
        self.name = name
        self.line = line
        self.scope = scope
        self.args_decl = args_decl
        self.returnAddress = returnAddress
