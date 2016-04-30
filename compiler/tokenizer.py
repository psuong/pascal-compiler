from mmap import mmap
from sys import argv
from aenum import enum


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

    @staticmethod
    def open_pascal_file():
        with open(argv[1], 'r + b') as pascal_file:
            memory_mapped_file = mmap(pascal_file.fileno(), 0)
        return memory_mapped_file


class Scanner:
    def __init__(self):
        self.memory_mapped_file = None
        self.current_state = None
        self.word = ''
        self.scanner_states = enum('NORMAL_CASE', 'STRING_CASE', 'DIGIT_CASE', 'LETTER_CASE', 'COMMENT_CASE')

        # TODO: Read through the memory mapped file and parse each "word"
        # TODO: Letter Case: Keep adding a letter to the word when a letter is scanned
        # TODO: Digit Case: Keep adding a number when a # is being read.
        # TODO: Digit case: Check for a real/floating point number.
        # TODO: String Case: Ignore until a string closer is read.
        # TODO: Comment Case: Ignore until end of line or a comment closer is read.
        # TODO: Delimiter case: Check if the word exists in any of the tokens.

