from sys import argv
from mmap import mmap


character_list = 'abcdefghijklmnopqrstuvwxyz'


def open_pascal_file():

    with open(argv[1], 'r+b') as pascal_file:
        # Map the entire file to memory
        mem_mapped_file = mmap(pascal_file.fileno(), 0)
        word = ''
        for line in mem_mapped_file:
            for char in line:
                if char in character_list:
                    word += char


if __name__ == '__main__':
    open_pascal_file()
