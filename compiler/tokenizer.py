from mmap import mmap
from sys import argv


class Token:
    def __init__(self):
        self.TK_OPERATORS = {
            '(': 'TK_OPEN_PARENTH',
            ')': 'TK_CLOSE_PARENTH',
            '.': 'TK_DOT',
            ';': 'TK_SEMI_COLON',
            ':': 'TK_COLON',
            '+': 'TK_PLUS',
            '-': 'TK_MINUS',
            '/': 'TK_DIVIDE',
            '*': 'TK_MULTIPLY',
            '=': 'TK_EQUAL',
            ',': 'TK_COMMA',
            '>': 'TK_GREATER',
            '>=': 'TK_GREATER_EQ',
            '<': 'TK_LESS',
            '<=': 'TK_LESS_EQ',
            ':=': 'TK_ASSIGNMENT'
        }

        self.TK_KEYWORDS = self.keyword_setup()
        self.TK_FILE = 'TK_EOF'
        self.TK_DIGIT = {
            '.': 'TK_REAL_LITERAL',
            'integer': 'TK_INTEGER_LITERAL'
        }
        self.TK_DATATYPES = {
            'string': 'TK_STRING',
            'real': 'TK_REAL',
            'integer': 'TK_INTEGER',
            'boolean': 'TK_BOOLEAN',
            'char': 'TK_CHARACTER'
        }

        self.TK_VAR = 'TK_A_VAR'
        self.TK_STRING = 'TK_STRING_LIT'
        self.TK_ID = 'TK_IDENTIFIER'

    @staticmethod
    def keyword_setup():
        keyword_dict = {}
        with open('compiler/keywords.txt', 'r') as keyword_file:
            for line in keyword_file:
                keyword_dict[line.rstrip()] = 'TK_KEYWORD_%s' % (line.upper())
        return keyword_dict


class FileManager:
    def __init__(self):
        self.pascal_file = self.open_pascal_file()

    def open_pascal_file(self):
        with open(argv[1], 'r + b') as pascal_file:
            memory_mapped_file = mmap(pascal_file.fileno(), 0)
        return memory_mapped_file


class Scanner:
    def __init__(self):
        memory_mapped_file = None
    pass
