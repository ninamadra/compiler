class SymbolTable:

    def __init__(self):
        self.variables = []
        self.arrays = []
        self.procedures = []
        self.mem_current = 0

    def addVariable(self, name, scope):
        self.checkRedeclaration(name, scope)
        self.variables.append(Variable(name, self.assignAddress(1), scope))

    def addArray(self, name, scope, size):
        self.checkRedeclaration(name, scope)
        self.arrays.append(Array(name, self.assignAddress(size), scope, size))

    def addProcedure(self, name, line):
        for procedure in self.procedures:
            if procedure.name == name:
                raise Exception(f"Procedure {name} already exists")
        self.procedures.append(Procedure(name, line))

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
        raise Exception(f"Variable '{name}' not found in scope '{scope}'")

    def getArray(self, name, scope):
        for array in self.arrays:
            if array.name == name and array.scope == scope:
                return array
        raise Exception(f"Array '{name}' not found in scope '{scope}'")

    def getProcedure(self, name):
        for procedure in self.procedures:
            if procedure.name == name:
                return procedure
        return Exception(f"Procedure '{name}' does not exist'")


class Variable:
    def __init__(self, name, address, scope, isInitialized=False):
        self.name = name
        self.address = address
        self.scope = scope


class Array:
    def __init__(self, name, address, scope, size):
        self.name = name
        self.address = address
        self.scope = scope
        self.size = size


class Procedure:
    def __init__(self, name, line):
        self.name = name
        self.address = line
