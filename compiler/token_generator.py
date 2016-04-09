from sys import argv
from mmap import mmap
from tokenizer import Token
from aenum import Enum

# Global variables to pass into the other parts of the compiler
COL_NUM = 0
LINE_NUM = 0
TOKEN_VALUE = None
TOKEN_TYPE = None

TOKEN_LIST = []


def open_pascal_file():
    """
    Opens the pascal file and loads the pascal file into memory.
    :return: memory mapped file
    """
    with open(argv[1], 'r + b') as pascal_file:
        # Map the entire pascal file to memory
        memory_mapped_file = mmap(pascal_file.fileno(), 0)

    return memory_mapped_file


def scan_pascal_file(mem_map):
    """
    Scans the memory mapped file and yield a token, value, and position.

    :param mem_map: mmap
    :return: (token, value, position)
    """
    token = Token()
    # Set up the token object
    token.TK_Keywords = token.tk_keyword_setup

    # Local variables for line number
    col_num = 0
    line_num = 0

    scanner_state = Enum('ScannerState', 'NORMAL_CASE STRING_CASE')
    current_state = scanner_state.NORMAL_CASE

    # Variable below allows building a word
    word = ''

    for index in range(0, len(mem_map) - 1):
        col_num += 1
        char = mem_map[index]

        if current_state is scanner_state.NORMAL_CASE:
            if char.isalpha():
                word += char
            elif char.isdigit():
                word += char
            elif char is ' ':
                if word in token.TK_Keywords.keys():
                    assign_token_values(token.TK_Keywords[word],
                                        word,
                                        col_num,
                                        line_num,
                                        True)
                word = ''
            elif char is '\n':
                col_num = 0
                line_num += 1
                if word in token.TK_Keywords.keys():
                    assign_token_values(token.TK_Keywords[word],
                                        word,
                                        col_num,
                                        line_num,
                                        True)
                word = ''

            elif char is ':':
                if mem_map[index + 1] is '=':
                    index += 1
                    word = '' + char + mem_map[index]
                    assign_token_values(token.TK_Operators[word],
                                        word,
                                        col_num,
                                        line_num,
                                        True)
                word = ''
            elif char in token.TK_Operators.keys():
                if word in token.TK_Keywords.keys():
                    assign_token_values(token.TK_Keywords[word],
                                        word,
                                        col_num,
                                        line_num,
                                        True)
                assign_token_values(token.TK_Operators[char],
                                    char,
                                    col_num,
                                    line_num,
                                    True)
                word = ''
            elif char == '\'' or char == '\"':
                current_state = scanner_state.STRING_CASE
                word = '' + char
        elif current_state is scanner_state.STRING_CASE:
            word += char
            if char == '\'' or char == '\"':
                assign_token_values(token.TK_Keywords['string'],
                                    word,
                                    col_num,
                                    line_num,
                                    True)
                word = ''
                current_state = scanner_state.NORMAL_CASE

    assign_token_values(token.TK_File['EOF'],
                        'EOF',
                        col_num,
                        line_num,
                        True)


def assign_token_values(token_type,
                        token_value,
                        col_num,
                        line_num,
                        should_print=False):
    """
    Assigns the global token variables.
    :param line_num: The current row the iterator is at.
    :param col_num: The current index the iterator is at.
    :param token_type: The type of token it is based on the Token class.
    :param token_value: The value of the token associated with the token_type.
    :param should_print: bool; Should the function print the tuple?
    :return: tuple
    """
    global COL_NUM
    global LINE_NUM
    global TOKEN_VALUE
    global TOKEN_TYPE
    global TOKEN_LIST

    TOKEN_VALUE = token_value
    TOKEN_TYPE = token_type
    COL_NUM = col_num
    LINE_NUM = line_num
    if should_print:
        print (TOKEN_TYPE, TOKEN_VALUE, COL_NUM, LINE_NUM)

    # Add all the tuples to a universal list
    TOKEN_LIST.append((TOKEN_TYPE, TOKEN_VALUE, COL_NUM, LINE_NUM))
    return TOKEN_TYPE, TOKEN_VALUE, COL_NUM, LINE_NUM


def print_memory_mapped_file(mem_map):
    """
    Prints the memory_mapped_file.

    :param mem_map: mmap
    """
    for line in iter(mem_map.readline, ''):
        print line


if __name__ == '__main__':
    scan_pascal_file(open_pascal_file())
