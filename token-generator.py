from sys import argv
from mmap import mmap

# Global variables to pass into the other parts of the compiler
GLOBAL_COL_NUM = 0
GLOBAL_LINE_NUM = 0


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
    # TODO: Do logic processing on each word parsed out of the pascal file.
    character_list = 'abcdefghjklmnopqrstuvwxyz'
    # TODO: Complete the list of special characters
    special_characters = '();.'

    global GLOBAL_COL_NUM
    global GLOBAL_LINE_NUM

    # Variable below allows building a word
    word = ''
    for char in mem_map:
        GLOBAL_COL_NUM += 1
        if char.isalpha():
            word += char
        elif char is ' ':
            print '%s | Line: %s | Col: %s' % (word, GLOBAL_LINE_NUM, GLOBAL_COL_NUM - len(word))
            word = ''
        elif char == '\n':
            GLOBAL_COL_NUM = 0
            GLOBAL_LINE_NUM += 1
            print '%s | Line: %s | Col: %s' % (word, GLOBAL_LINE_NUM, GLOBAL_COL_NUM - len(word))
            word = ''
        elif char in special_characters:
            print '%s | Line: %s | Col: %s' % (char, GLOBAL_LINE_NUM, GLOBAL_COL_NUM)
            word = ''


def print_memory_mapped_file(mem_map):
    """
    Prints the memory_mapped_file.

    :param mem_map: mmap
    """
    for line in iter(mem_map.readline, ''):
        print line


if __name__ == '__main__':
    # scan_pascal_file(open_pascal_file())
    print_memory_mapped_file(open_pascal_file())
