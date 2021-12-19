import sys
from parser.parse import Parser

if __name__ == '__main__':
    input_path = sys.argv[2]
    output_path = sys.argv[4]
    table_path = sys.argv[6]

    parser = Parser(input_path, output_path)
    try:
        parser.parse()
    except StopIteration:
        with open(output_path, 'r') as f:
            f.write('Syntax is correct!')
    except Exception as e:
        print(f"Compilation failed with {e.args[0]} errors.")
        with open(output_path, 'r') as f:
            f.write('Syntax is wrong!')
