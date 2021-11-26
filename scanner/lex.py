import os

from ply import lex
import statics
import os


class Lexer:
    def __init__(self, filename):
        self.filename = filename
        self.lexer = lex.lex(module=self, debug=True)

    def tokenize(self):
        file = open(self.filename, 'r')
        return self.lexer.input(file.read())

    tokens = statics.tokens

    # TOKENS
    t_STRING = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'=='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COLON = r','
    t_SEMICOLON = r';'
    t_DOT = r'\.'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'--'
    t_ASSIGNMENT = r'='
    t_ADDITION_ASSIGNMENT = r'\+='
    t_SUBTRACTION_ASSIGNMENT = r'-='
    t_MULTIPLICATION_ASSIGNMENT = r'\*='
    t_DIVISION_ASSIGNMENT = r'/='
    t_BITWISE_AND = r'&'
    t_BITWISE_OR = r'\|'
    t_BITWISE_XOR = r'\^'
    t_GREATER_THAN = r'>'
    t_LESS_THAN = r'<'
    t_GREATER_THAN_EQUALS = r'>='
    t_LESS_THAN_EQUALS = r'<='
    t_NOT_EQUALS = r'!='
    t_MOD = r'%'

    # SPECIAL CHARS
    t_DOUBLE_QUOTATION = r'\"'
    t_QUOTATION = r'\''
    t_TAB = r'\t'
    t_BACKSLASH = r'\\'

    t_SPACE = r'\s+'

    # RESERVED WORDS
    t_LET = r'let'
    t_VOID = r'void'
    t_INT = r'int'
    t_REAL = r'real'
    t_BOOL = r'bool'
    t_STRING_KEYWORD = r'string'
    t_STATIC = r'static'
    t_CLASS = r'class'
    t_FOR = r'for'
    t_ROF = r'rof'
    t_LOOP = r'loop'
    t_POOL = r'pool'
    t_WHILE = r'while'
    t_BREAK = r'break'
    t_CONTINUE = r'continue'
    t_IF = r'if'
    t_FI = r'fi'
    t_ELSE = r'else'
    t_THEN = r'then'
    t_NEW = r'new'
    t_ARRAY = r'Array'
    t_RETURN = r'return'
    t_IN_STRING = r'in_string'
    t_IN_INT = r'in_int'
    t_PRINT = r'print'
    t_LEN = r'len'

    t_ignore = ''

    def t_REAL_NUMBER(self, t):
        r'([-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+))|0x[0-9A-F]+'
        try:
            t.value = float(t.value)
        except ValueError:
            t.value = float.fromhex(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_COMMENT(self, t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        t.type = 'COMMENT'
        return t

    def t_NEW_LINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = 'NEW_LINE'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = statics.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


