# mv@panix.com : zip
from tokenizer import FileManager, Scanner, TOKEN_LIST
from parsermodule import ParserModule
from emulator import EmulatorModule


def load_pascal_file():
    pascal_file = FileManager()
    scanner = Scanner()
    parser = ParserModule(iter(TOKEN_LIST))

    scanner.memory_mapped_file = pascal_file.pascal_file

    scanner.read_memory_file()
    parser.parse()

    emulator = EmulatorModule(parser.byte_array)

    emulator.execute()


if __name__ == '__main__':
    load_pascal_file()
