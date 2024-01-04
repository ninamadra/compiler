from lexer import MyLexer
from parser import MyParser
from generator import MyGenerator


class Compiler:
    def __init__(self):
        self.lexer = MyLexer()
        self.parser = MyParser()
        self.generator = MyGenerator()

    def compile_and_print(self, source_code):
        try:
            tokens = self.lexer.tokenize(source_code)
            ast = self.parser.parse(tokens)
            self.generator.generate(ast)

        except Exception as e:
            print(f"Compilation error: {e}")


if __name__ == "__main__":
    compiler = Compiler()

    # Example source code
    code = """
        PROGRAM IS
        a
        IN
            a := 5;
            WRITE a;
        END
    """

    # Compile and print generated code
    compiler.compile_and_print(code)
