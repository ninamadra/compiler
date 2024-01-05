import sys
from lexer import MyLexer
from parser import MyParser


class Compiler:
    def __init__(self):
        self.lexer = MyLexer()
        self.parser = MyParser()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('Usage: python3 compiler.py <plik_in> <plik_out>')
        exit(1)

    path_in = sys.argv[1]
    path_out = sys.argv[2]
    lexer = MyLexer()
    parser = MyParser()

    with open(path_in) as file:
        text = file.read()
        code = parser.parse(lexer.tokenize(text))
    with open(path_out, "w") as file:
        file.write(code)
    print(f'Wynik kompilacji pliku {path_in} zapisany w pliku {path_out}.')
