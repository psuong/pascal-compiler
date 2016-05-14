from tokenizer import Token, FileManager, Scanner

def load_pascal_file():
    pascal_file = FileManager()
    scanner = Scanner()

    scanner.memory_mapped_file = pascal_file.pascal_file

    scanner.read_memory_file()


if __name__ == '__main__':
    load_pascal_file()
