from sys import argv
from mmap import mmap


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
    """
    pass


def print_memory_mapped_file(mem_map):
    """
    Prints the memory_mapped_file.

    :param mem_map: mmap
    """
    for line in iter(mem_map.readline, ''):
        print line


if __name__ == '__main__':
    print_memory_mapped_file(open_pascal_file())
