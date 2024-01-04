import unittest
from lexer import MyLexer
import os


class TestMyLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = MyLexer()

    def test_all_files(self):
        test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data', 'lexer'))
        input_files = [f for f in os.listdir(test_data_dir) if f.endswith('.in')]

        for input_file in input_files:
            with self.subTest(input_file=input_file):
                input_path = os.path.join(test_data_dir, input_file)
                expected_output_path = os.path.join(test_data_dir, input_file.replace('.in', '.out'))

                with open(input_path, 'r') as f:
                    code = f.read()

                with open(expected_output_path, 'r') as f:
                    expected_tokens = eval(f.read())

                self.assertLexerTokens(code, expected_tokens)

    def assertLexerTokens(self, code, expected_tokens):
        tokens = list(self.lexer.tokenize(code))
        for expected_token, actual_token in zip(expected_tokens, tokens):
            self.assertEqual(expected_token[0], actual_token.type)
            self.assertEqual(str(expected_token[1]), actual_token.value)


if __name__ == '__main__':
    unittest.main()
