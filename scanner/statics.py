reserved = {
    'let': 'LET',
    'void': 'VOID',
    'int': 'INT',
    'real': 'REAL',
    'bool': 'BOOL',
    'string': 'STRING_KEYWORD',
    'static': 'STATIC',
    'class': 'CLASS',
    'for': 'FOR',
    'rof': 'ROF',
    'loop': 'LOOP',
    'pool': 'POOL',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'if': 'IF',
    'fi': 'FI',
    'else': 'ELSE',
    'then': 'THEN',
    'new': 'NEW',
    'Array': 'ARRAY',
    'return': 'RETURN',
    'in_string': 'IN_STRING',
    'in_int': 'IN_INT',
    'print': 'PRINT',
    'len': 'LEN',
}

special_chars = [
    'DOUBLE_QUOTATION',
    'QUOTATION',
    'NEW_LINE',
    'TAB',
    'BACKSLASH'
]

operators = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'EQUALS',
    'NOT_EQUALS',
    'LESS_THAN',
    'LESS_THAN_EQUALS',
    'GREATER_THAN',
    'GREATER_THAN_EQUALS',
    'AND',
    'OR',
    'NOT',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COLON',
    'DOT',
    'ADDITION_ASSIGNMENT',
    'SUBTRACTION_ASSIGNMENT',
    'MULTIPLICATION_ASSIGNMENT',
    'DIVISION_ASSIGNMENT',
    'INCREMENT',
    'DECREMENT',
    'ASSIGNMENT',
    'BITWISE_AND',
    'BITWISE_OR',
    'BITWISE_XOR',
]

tokens = [
    'ID',
    'INTEGER',
    'REAL_NUMBER',
    'STRING',
    'IDENTIFIER',
    'COMMENT',

]

tokens += list(reserved.values()) + special_chars + operators

css = """
    <style>
    .background {
        background-color: #222222;
    }
    .reserved_keyword {
        color: #FC618D;
    }
    .identifier {
        color: #FFFFFF;
    }
    .integer_number {
        color: #F59762;
    }
    .float_number {
        color: #F59762;
        font-style: italic;
    }
    .string {
        color: #FCE566;
    }

    .special_char {
        color: #EE82EE;
        font-style: italic;
    }

    .comment {
        color: #69676C;
    }

    .operator {
        color: #00FFFF;
    }

    .error {
        color: #FF0000;
    }
    </style>

"""

class_type_map = {
    "reserved_keyword": list(reserved.values()),
    "identifier": ['ID'],
    "integer_number": ['INTEGER'],
    "float_number": ['REAL_NUMBER'],
    'special_char': special_chars,
    "comment": ['COMMENT'],
    "operator": operators,
    "error": ['ERROR'],

}
