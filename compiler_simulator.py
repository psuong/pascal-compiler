# mv@panix.com : zip
from tokenizer import FileManager, Scanner, TOKEN_LIST, print_token_list
from parser_module import ParserModule
from emulate_module import EmulatorModule


def load_pascal_file():
    # Create the file manager
    pascal_file = FileManager()

    # Create the scanner
    scanner = Scanner()

    # Assign the memory mapped file from the FileManager
    scanner.memory_mapped_file = pascal_file.pascal_file

    # Read the memory file and produce tokens
    scanner.read_memory_file()

    # Print the token list, uncomment if you would like to see the output.
    # print_token_list()

    # Assign the token list to the parser
    parser = ParserModule(iter(TOKEN_LIST))

    # Parse the tokens
    parser.parse()

    # Print out all tokens being matched, uncomment if you would like to see it happen.
    # parser.print_token_matching()

    # Create the emulator module
    emulator = EmulatorModule(parser.byte_array)

    # Emulate the compiler
    emulator.execute()


if __name__ == '__main__':
    load_pascal_file()
