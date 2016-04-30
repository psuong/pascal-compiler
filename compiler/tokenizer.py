from mmap import mmap
from sys import argv
from aenum import Enum


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
        self.scanner_state = Enum('ScannerStates', 'letter digit')

    def read_memory_file(self):
        """
        Reads the memory_mapped_file and determines what tokens to return based on the word.
        :return: None
        """
        self.current_state = self.get_initial_state(self.memory_mapped_file[0])

        for index in range(0, len(self.memory_mapped_file) + 1):
            # Assign the index of he memory mapped file to a variable for ease
            char = self.memory_mapped_file[index]

            # TODO: Letter Case: Keep adding a letter to the word when a letter is scanned
            if char.isalpha():
                self.word += char
            # TODO: Digit Case: Keep adding a number when a # is being read.
            # TODO: Digit case: Check for a real/floating point number.
            elif char.isdigit():
                self.word += char
        # TODO: Read through the memory mapped file and parse each "word"
        # TODO: String Case: Ignore until a string closer is read.
        # TODO: Comment Case: Ignore until end of line or a comment closer is read.
        # TODO: Delimiter case: Check if the word exists in any of the tokens.

    def get_initial_state(self, char):
        """
        Gets the first initial state of the pascal file.
        :param char: string
        :return: ScannerState
        """
        initial_char = self.memory_mapped_file[0]
        if initial_char.isalpha():
            return self.scanner_state.letter
        elif initial_char.isdigit():
            return self.scanner_state.digit

    def read_letter(self, char):
        self.word += char
        if not char.isalpha():
            pass
