import sys
from lexer import MyLexer
from parser import MyParser


def process_labels(input_code):
    labels = []
    lines = input_code.split('\n')

    for i, line in enumerate(lines):
        labels_in_line = []
        while line.strip().startswith("label"):
            label = line.split()[0]
            labels_in_line.append((label, i))
            line = line.replace(label, "", 1).strip()

        labels.extend(labels_in_line)
        lines[i] = line

    for i, line in enumerate(lines):
        for label, line_number in labels:
            words = line.split()
            if len(words) >= 2 and words[1] == label:
                lines[i] = ' '.join([words[0], str(line_number)] + words[2:])

    result_code = '\n'.join(lines)
    return result_code


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('Usage: python3 compiler.py <in_file> <out_file>')
        exit(1)

    path_in = sys.argv[1]
    path_out = sys.argv[2]
    lexer = MyLexer()
    parser = MyParser()

    with open(path_in) as file:
        text = file.read()
        code = process_labels(parser.parse(lexer.tokenize(text)))

    with open(path_out, "w") as file:
        file.write(code)
    print(f'{path_in} compilation result was saved to the file {path_out}.')
