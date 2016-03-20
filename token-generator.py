from sys import argv
from mmap import mmap
from token import tk_keyword_setup, Token

# Global variables to pass into the other parts of the compiler
GLOBAL_COL_NUM = 0
GLOBAL_LINE_NUM = 0
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
    # TODO: Return a token type
    token = Token()
    # Set up the token object
    token.TK_Keywords = tk_keyword_setup()

    special_characters = '();.'

    # Set of global variables to access

    global GLOBAL_COL_NUM
    global GLOBAL_LINE_NUM
    global TOKEN_VALUE
    global TOKEN_TYPE

    # Variable below allows building a word
    word = ''
    for char in mem_map:
        GLOBAL_COL_NUM += 1
        # Builds the word in order to check if it is a keyword.
        if char.isalpha():
            word += char
        elif char is ' ':
            if word in token.TK_Keywords.keys():
                print '%s, %s, %s, %s' % (word, token.TK_Keywords[word], GLOBAL_COL_NUM, GLOBAL_LINE_NUM)
            # Reset the word
            word = ''
        # Case: If the char is a newline char, then reset the column no.
        # and increment the line no.
        elif char == '\n':
            GLOBAL_COL_NUM = 0
            GLOBAL_LINE_NUM += 1
            # print 'Col: %i, Line: %i' % (GLOBAL_COL_NUM, GLOBAL_LINE_NUM)
        elif char in special_characters:
            print '%s, %s, %s' % (char, GLOBAL_COL_NUM, GLOBAL_LINE_NUM)


def print_memory_mapped_file(mem_map):
    """
    Prints the memory_mapped_file.

    :param mem_map: mmap
    """
    for line in iter(mem_map.readline, ''):
        print line


if __name__ == '__main__':
    scan_pascal_file(open_pascal_file())
