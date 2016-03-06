from sys import argv
from mmap import mmap


def open_pascal_file():

    with open(argv[1], 'r+b') as pascal_file:
        # Map the entire file to memory
        mem_mapped_file = mmap(pascal_file.fileno(), 0)
        print mem_mapped_file.readline()


if __name__ == '__main__':
    open_pascal_file()
