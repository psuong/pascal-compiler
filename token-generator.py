from sys import argv
from mmap import mmap
from token import tk_keyword_setup, Token

# Global variables to pass into the other parts of the compiler
COL_NUM = 0
LINE_NUM = 0
TOKEN_VALUE = None
TOKEN_TYPE = None


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
    token.TK_Keywords = tk_keyword_setup()

    # Local variables for line number
    col_num = 0
    line_num = 0

    # Variable below allows building a word
    word = ''

    for char in mem_map:
        col_num += 1
        # While the scanner scans a letter continuously append it to the
        # `word` variable.
        if char.isalpha():
            word += char
        elif char is ' ':
            if word in token.TK_Keywords.keys():
                assign_token_values(token.TK_Keywords[word],
                                    word, col_num,
                                    line_num,
                                    True)
            # Reset the word
            word = ''
        # Case: If the char is a newline char, then reset the column no.
        # and increment the line no.
        elif char == '\n':
            col_num = 0
            line_num += 1
        # Case: If the char is one of the special chars (operators),
        # then return the tokens
        elif char in token.TK_Operators.keys():
            assign_token_values(token.TK_Operators[char],
                                char, col_num,
                                line_num,
                                True)
        elif char is '\'':
            # Reset the word
            word = ''
            # TODO: Check case string.
            pass


def assign_token_values(token_type,
                        token_value,
                        col_num,
                        line_num,
                        should_print=False):
    """
    Assigns the global token variables.
    :param token_type: The type of token it is based on the Token class.
    :param token_value: The value of the token associated with the token_type.
    :param should_print: bool; Should the function print the tuple?
    :return: tuple
    """
    global COL_NUM
    global LINE_NUM
    global TOKEN_VALUE
    global TOKEN_TYPE

    TOKEN_VALUE = token_value
    TOKEN_TYPE = token_type
    COL_NUM = col_num
    LINE_NUM = line_num
    if should_print:
        print (TOKEN_TYPE, TOKEN_VALUE, COL_NUM, LINE_NUM)

    return (TOKEN_TYPE, TOKEN_VALUE, COL_NUM, LINE_NUM)


def print_memory_mapped_file(mem_map):
    """
    Prints the memory_mapped_file.

    :param mem_map: mmap
    """
    for line in iter(mem_map.readline, ''):
        print line


if __name__ == '__main__':
    scan_pascal_file(open_pascal_file())
