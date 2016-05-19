from mmap import mmap
from sys import argv
from aenum import Enum

TOKEN_LIST = []
CONST_TK_ID = 'TK_IDENTIFIER'
TK_OPERATOR = 'TK_OPERATOR'


class TokenContainer(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


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
            '<>': 'TK_NOT_EQUAL',
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
            'real': 'TK_REAL_LITERAL',
            'integer': 'TK_INTEGER_LITERAL'
        }
        self.TK_DATATYPES = {
            'string': 'TK_DATATYPE_STRING',
            'real': 'TK_DATATYPE_REAL',
            'integer': 'TK_DATATYPE_INTEGER',
            'boolean': 'TK_DATATYPE_BOOLEAN',
            'char': 'TK_DATATYPE_CHARACTER'
        }

        self.TK_VAR = 'TK_A_VAR'
        self.TK_STRING = 'TK_STRING_LIT'
        self.TK_ID = CONST_TK_ID

    @staticmethod
    def keyword_setup():
        """
        Opens the keywords.txt file and reads it to create the dictionary containing all of
        the pascal keywords.
        :return: None
        """
        keyword_dict = {}
        with open('keywords.txt', 'r') as keyword_file:
            for line in keyword_file:
                keyword_dict[line.rstrip()] = 'TK_KEYWORD_%s' % (line.upper().strip('\n'))
        return keyword_dict

    def get_token(self, word):
        """
        Returns a token type based on the word being parsed.
        :param word: string
        :return: Token
        """
        # TODO: Finish the rest of the token retrieving.
        if self.TK_DATATYPES.get(word) is not None:
            return self.TK_DATATYPES[word]
        elif self.TK_KEYWORDS.get(word) is not None:
            return self.TK_KEYWORDS[word]
        elif self.TK_OPERATORS.get(word) is not None:
            return self.TK_OPERATORS[word]
        else:
            return self.TK_ID


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
        self.special_chars = ',./<>?:;\[]{}!@#$%^&*()-_+='
        self.word = ''
        self.scanner_state = Enum('ScannerStates', 'letter digit operator delimiter string')
        self.token = Token()

    def read_memory_file(self):
        """
        Reads the memory_mapped_file and determines what tokens to return based on the word.
        :return: None
        """
        self.current_state = self.get_initial_state(self.memory_mapped_file[0])
        for index in range(0, len(self.memory_mapped_file)):
            char = self.memory_mapped_file[index]
            if self.current_state is self.scanner_state.letter:
                self.read_letter(char, index)
            elif self.current_state is self.scanner_state.digit:
                self.read_number(char, index)
            elif self.current_state is self.scanner_state.operator:
                self.read_operator(char, index)
            elif self.current_state is self.scanner_state.delimiter:
                self.read_delimiter(char, index)
            elif self.current_state is self.scanner_state.string:
                self.read_string(char, index)

        TOKEN_LIST.append(TokenContainer(self.token.TK_FILE, 'EOF'))

        for each in TOKEN_LIST:
            print 'ID: %s, Value: %s' % (each.token, each.value)

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
        try:
            next_char = self.memory_mapped_file[index + 1]
        except IndexError:
            next_char = self.memory_mapped_file[index]
        if next_char.isalpha():
            return self.scanner_state.letter
        elif next_char.isdigit():
            return self.scanner_state.digit
        elif next_char in self.delimiter_chars:
            return self.scanner_state.delimiter
        elif next_char == '\'' or next_char == '"':
            return self.scanner_state.string
        elif next_char in self.special_chars:
            return self.scanner_state.operator

    def read_letter(self, char, index):
        """
        Appends a character to a word and checks the state.
        :param char: string
        :param index: int
        :return: None
        """
        if char.isalpha():
            self.word += char
            self.current_state = self.scanner_state.letter
        elif char.isdigit():
            self.word += char
            self.current_state = self.scanner_state.digit
        elif char in self.special_chars:
            TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
            self.word = char
            self.current_state = self.scanner_state.operator
        elif char in self.delimiter_chars:
            TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
            self.word = ''
            self.current_state = self.get_next_state(index)
            # print 'Next State: %s' % self.get_next_state(index)

    def read_number(self, char, index):
        """
        Continues to read a number until until a separate char is read. "." are
        ignored.
        :param char: string
        :param index: int
        :return: None
        """
        if char.isdigit():
            self.word += char
        elif char == '.' and char in self.special_chars:
            self.word += char
            self.current_state = self.scanner_state.digit
        elif char != '.' and char in self.special_chars:
            if '.' in self.word:
                TOKEN_LIST.append(TokenContainer(self.token.TK_DATATYPES['real'], self.word))
                self.word = char
                self.current_state = self.scanner_state.operator
            else:
                TOKEN_LIST.append(TokenContainer(self.token.TK_DATATYPES['integer'], self.word))
                self.word = char
                self.current_state = self.scanner_state.operator
                # print 'State: %s \t Char: %s' % (self.current_state, self.memory_mapped_file[index + 1])
        elif char.isalpha():
            self.word += char
            TOKEN_LIST.append(TokenContainer(self.token.TK_ID, self.word))
            self.current_state = self.get_next_state(index)
        elif char in self.delimiter_chars:
            if '.' in self.word:
                TOKEN_LIST.append(TokenContainer(self.token.TK_DATATYPES['real'], self.word))
                self.word = ''
                self.current_state = self.get_next_state(index)
            else:
                TOKEN_LIST.append(TokenContainer(self.token.TK_DATATYPES['integer'], self.word))
                self.word = ''
                self.current_state = self.get_next_state(index)

    def read_operator(self, char, index):
        """
        Appends a character to a word and checks the state.
        :param char: string
        :param index: int
        :return: None
        """
        if char in self.special_chars:
            if '(' in self.word or ')' in self.word and char == ';':
                TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
                self.word = char
            else:
                self.word += char
            self.current_state = self.scanner_state.operator
        elif char == '\'' or char == '"':
            TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
            self.word = char
            self.current_state = self.scanner_state.string
        elif char.isalpha():
            TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
            self.word = char
            self.current_state = self.scanner_state.letter
        elif char.isdigit():
            TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
            self.word = char
            self.current_state = self.get_next_state(index)
        elif char in self.delimiter_chars:
            TOKEN_LIST.append(TokenContainer(self.token.get_token(self.word), self.word))
            self.word = ''
            self.current_state = self.get_next_state(index)

    def read_delimiter(self, char, index):
        """
        Reads any kind of delimiter characters and updates the state.
        :param char: string
        :param index: int
        :return: None
        """
        # Keep getting the next state until you get something other than a delimiter
        if char in self.delimiter_chars:
            self.current_state = self.get_next_state(index)

    def read_string(self, char, index):
        """
        Reads any kind of char within a string until the string is closed.
        :param char: string
        :param index: int
        :return: None
        """
        self.word += char
        if char == '\'' or char == '"':
            TOKEN_LIST.append(TokenContainer(self.token.TK_DATATYPES['string'], self.word))
            self.word = ''
            self.current_state = self.get_next_state(index)

    @staticmethod
    def print_word(word):
        """
        Static method which prints the given word.
        :param word:
        :return:
        """
        print word
