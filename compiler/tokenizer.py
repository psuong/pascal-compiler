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
        self.delimiter_chars = ' \n\t'
        self.word = ''
        self.scanner_state = Enum('ScannerStates', 'letter digit')

    def read_memory_file(self):
        """
        Reads the memory_mapped_file and determines what tokens to return based on the word.
        :return: None
        """
        self.current_state = self.get_initial_state(self.memory_mapped_file[0])

        for index in range(0, len(self.memory_mapped_file)):
            char = self.memory_mapped_file[index]
            if self.current_state is self.scanner_state.letter:
                self.read_letter(char)

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

    def get_next_state(self, index):
        """
        Scans the next character in the file and determines
        what the next state should be in the state machine.
        :param index: int
        :return: ScannerStates
        """
        next_char = self.memory_mapped_file[index + 1]
        if next_char.isalpha():
            return self.scanner_state.letter
        elif next_char.isdigit():
            return self.scanner_state.digit

    def read_letter(self, char):
        """
        Appends a character to a word and checks the state.
        :param char: string
        :return: None
        """
        self.word += char
        if char.isalpha():
            self.current_state = self.scanner_state.letter
        elif char.isdigit():
            self.current_state = self.scanner_state.digit
        elif char in self.delimiter_chars:
            word = self.word
            self.print_word(word)
            self.word = ''

    @staticmethod
    def print_word(self, word):
        print word
