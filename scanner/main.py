from scanner.lex import Lexer
from scanner.syntax_highlighter import SyntaxHighlighter


class Scanner:
    def __init__(self, input_file):
        self.file_name = input_file
        self.output_file = input_file + "output.html"
        self.lexer = Lexer(f'{self.file_name}')
        self.syntax_highlighter = SyntaxHighlighter()

    def run(self):
        self.lexer.tokenize()
        while True:
            token = self.lexer.lexer.token()
            if not token:
                break
            self.syntax_highlighter.highlight(token)
        self.syntax_highlighter.flush(self.output_file)


if __name__ == '__main__':
    scanner = Scanner("../tests/input1.cool")
    scanner.run()
    scanner = Scanner("../tests/input2.cool")
    scanner.run()
    scanner = Scanner("../tests/phase1_test1.cool")
    scanner.run()
    scanner = Scanner("../tests/phase1_test2.cool")
    scanner.run()