import csv
import os
from codegen.codegenrator import CodeGenerator
from scanner import Lexer
from utils import errors

START_STATE = 0


class Parser:
    def __init__(self, file_name, table_name):
        self.table = {}
        self.grammar = {}
        with open(file_name, 'r') as file:
            self.src_code = file.readlines()
        with open(table_name, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                state = int(row[0].strip())
                for i in range(1, len(row)):
                    prev_data = self.grammar.get((state, header[i].strip()))
                    if not prev_data or prev_data == 'ERROR':
                        self.grammar[(state, header[i].strip())] = row[i].strip()
        self.code_generator = CodeGenerator()

        self.lexer = Lexer(file_name)

    def parse(self):
        state = START_STATE
        parse_stack = []
        token_generator = self.lexer.get_token()
        token = next(token_generator)
        while True:
            if token is None:
                break
            while token.ptype in ['COMMENT', 'SPACE','NEW_LINE']:
                token = next(token_generator)
            print(state, token)
            data = self.grammar[(state, token.ptype)].split(' ')
            # print(data)
            if len(data) == 1:
                if data[0] == "ERROR":
                    raise errors.ParserException(errors.ParserException)
                else:
                    raise errors.ParserException(errors.INVALID_GRAMMAR)

            if len(data) == 2:
                if data[0] == "ACCEPT":
                    self.code_generator.generate_code(data[1], token)
                    print("Compilation completed with 0 errors.")
                    return
                elif data[0] == "REDUCE":
                    nxt_data = self.grammar[(parse_stack.pop(), data[1])].split(' ')
                    self.code_generator.generate_code(nxt_data[2], data[1])
                    state = int(nxt_data[1][1:])
                else:
                    raise errors.ParserException(errors.INVALID_GRAMMAR)
            if len(data) == 3:
                if data[0] == "SHIFT":
                    state = int(data[1][1:])
                    self.code_generator.generate_code(data[2], token)
                    token = next(token_generator)
                elif data[0] == "GOTO":
                    state = int(data[1][1:])
                    token = next(token_generator)
                elif data[0] == "PUSH_GOTO":
                    parse_stack.append(state)
                    self.code_generator.generate_code(data[2], token)
                    state = int(data[1][1:])

                else:
                    raise errors.ParserException(errors.INVALID_GRAMMAR)


filenames = next(os.walk('../tests_parser/in'), (None, None, []))[2]  # [] if no file
filenames = sorted(filenames)
p = Parser(f'../tests_parser/in/16_variables2.cool', '../table.csv')
try:
    p.parse()
except StopIteration:
    p.code_generator.flush("../out.s")
    raise  Exception()


filenames = next(os.walk('../tests_parser/in'), (None, None, []))[2]  # [] if no file
filenames = sorted(filenames)
for f in filenames:
    try:
        p = Parser(f'../tests_parser/in/{f}', '../table.csv')
        p.parse()
    except StopIteration:
        print(f, "Correct")
        continue
        # print("Compilation completed with 0 errors.", f)
    except Exception as e:
        # print(f"Compilation failed with {e.args[0]} errors.", f)
        with open(f'../tests_parser/out/{f.split(".")[0]}.out', 'r') as file:
            res = file.read()
            if res != 'Syntax is wrong!':
                print(f"Expected: Syntax is wrong!\nGot: {res}", f)



