class SymbolTable:

    def __init__(self):
        self.variables = []
        self.arrays = []
        self.procedures = []
        self.mem_current = 0

    def addVariable(self, name, scope, isPointer, line, isInitialized=False):
        self.checkRedeclaration(name, scope, line)
        variable = Variable(name, self.assignAddress(1), scope, isPointer, isInitialized)
        self.variables.append(variable)
        return variable

    def addArray(self, name, scope, size, isPointer, line):
        self.checkRedeclaration(name, scope, line)
        array = Array(name, self.assignAddress(size), scope, size, isPointer)
        self.arrays.append(array)
        return array

    def addProcedure(self, name, line, scope, args_decl, lineno, isDeclared):
        for procedure in self.procedures:
            if procedure.name == name:
                raise Exception(f"Procedure {name} already exists, line: {lineno}.")
        procedure = Procedure(name, line, scope, args_decl, self.addVariable("r_" + name, scope, False, lineno).address, isDeclared)
        self.procedures.append(procedure)
        return procedure

    def markProceduresDeclared(self):
        for procedure in self.procedures:
            procedure.isDeclared = True

    def markVariableInitialized(self, name, scope):
        for variable in self.variables:
            if variable.name == name and variable.scope == scope:
                variable.isInitialized = True

    def checkRedeclaration(self, name, scope, line):
        for var in self.variables:
            if var.name == name and var.scope == scope:
                raise Exception(f"Variable with name '{name}' already declared in this scope, at line {line}.")
        for arr in self.arrays:
            if arr.name == name and arr.scope == scope:
                raise Exception(f"Array with name '{name}' already declared in this scope, at line {line}.")

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

    def getProcedure(self, name, line):
        for procedure in self.procedures:
            if procedure.name == name:
                if procedure.isDeclared is False:
                    raise Exception(f"Recursive procedure call for procedure '{procedure.name}' at line {line}.")
                return procedure
        raise Exception(f"Procedure '{name}' does not exist, line: {line}.")

    def readSymbols(self):
        print("variables")
        for var in self.variables:
            print("name: ", var.name, " address: ", var.address, " scope: ", var.scope, " isPointer: ", var.isPointer, " isInitialized: " + str(var.isInitialized))
        print("arrays")
        for var in self.arrays:
            print("name: ", var.name, " address: ", var.address, " scope: ", var.scope, " size: ", var.size, " isPointer: ", var.isPointer)
        print("procedures")
        for procedure in self.procedures:
            print("name: ", procedure.name, " label: ", procedure.line, "args_decl: ", str(procedure.args_decl), "return address: ", procedure.returnAddress, "declared: ", procedure.isDeclared)


class Variable:
    def __init__(self, name, address, scope, isPointer=False, isInitialized=False):
        self.name = name
        self.address = address
        self.scope = scope
        self.isPointer = isPointer
        self.isInitialized = isInitialized


class Array:
    def __init__(self, name, address, scope, size, isPointer=False):
        self.name = name
        self.address = address
        self.scope = scope
        self.size = size
        self.isPointer = isPointer


class Procedure:
    def __init__(self, name, line, scope, args_decl, returnAddress, isDeclared):
        self.name = name
        self.line = line
        self.scope = scope
        self.args_decl = args_decl
        self.returnAddress = returnAddress
        self.isDeclared = isDeclared
