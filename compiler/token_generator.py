from tokenizer import Token, FileManager, Scanner
from sys import argv
            word += char
            if not char.isdigit() and word.isdigit():
                assign_token_values(token.TK_Digit['integer'],
                                    word,
                                    col_num,
                                    line_num,
                                    True)
                word = ''
                current_state = scanner_state.DIGIT_CASE
            elif not char.isdigit() and '.' in word:
                assign_token_values(token.TK_Digit['.'],
                                    word,
                                    col_num,
                                    line_num,
                                    True)
                word = ''
                current_state = scanner_state.DIGIT_CASE
            elif char.isalpha():
                word = char
                current_state = scanner_state.NORMAL_CASE


def load_pascal_file():
    pascal_file = FileManager()
    scanner = Scanner()

    scanner.memory_mapped_file = pascal_file.pascal_file

    scanner.read_memory_file()


if __name__ == '__main__':
    load_pascal_file()
