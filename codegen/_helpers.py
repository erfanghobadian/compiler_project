def math_op_output_type(op, type1, type2):
    sops = ['*', '-', '+', '&' , '&', '|', '^', '%']
    print(op, type1, type2)
    if op in sops:
        if type1 in ["REAL_NUMBER", "REAL"] or type2 in ["REAL_NUMBER", "REAL"]:
            return "REAL"
        elif type1 in ["INTEGER", "INT"] and type2 in ["INTEGER", "INT"]:
            return "INT"
    elif op == '/':
        return "REAL"
    elif op in ['&&', '||']:
        if type1 in ['BOOL', 'BOOLEAN'] and type2 in ['BOOL', 'BOOLEAN']:
            return 'BOOL'


def check_type_mismatch(type1, type2):
    reals = {'REAL', 'REAL_NUMBER'}
    ints = {'INTEGER', 'INT'}
    strings = {'STRING', 'STRING_KEYWORD'}
    bools = {'BOOL', 'BOOLEAN'}
    if type1 in reals and type2 in reals:
        is_valid = True
    elif type1 in ints and type2 in ints:
        is_valid = True
    elif type1 in strings and type2 in strings:
        is_valid = True
    elif type1 in bools and type2 in bools:
        is_valid = True
    else:
        is_valid = type1 == type2

    if not is_valid:
        raise TypeError("Type mismatch: {} and {}".format(type1, type2))


operation_map = {
    '*': 'mul',
    '/': 'div',
    '+': 'add',
    '-': 'sub',
    '&&': 'and',
    '&': 'and',
    '|': 'or',
    '||': 'or',
    '<': 'slt',
    '>': 'sgt',
    '<=': 'sle',
    '>=': 'sge',
    '==': 'seq',
    '!=': 'sne',
}

type_asm_map = {
    '.word': 'w',
    '.byte': 'b',
    '.asciiz': 'a',
}
