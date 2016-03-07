class Token:
    def __init__(self):
        self.TK_Operators = {
            '(': TK_OPEN_PARENTH,
            ')': TK_CLOSE_PARENTH,
            '.': TK_DOT,
            ';': TK_SEMI_COLON,
            '+': TK_PLUS,
            '-': TK_MINIS,
            '/': TK_DIVIDE,
            '*': TK_MULTIPLY,
            '=': TK_EQUAL,
            ',': TK_COMMA,
            '>': TK_GREATER,
            '<': TK_LESS
        }
        self.TK_Characters = ['abcdefghijklmnoprqstuvwxyz']
        self.TK_Keywords = {}
