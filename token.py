class Token:
    def __init__(self):
        self.TK_Operators = {
            '(': 'TK_OPEN_PARENTH',
            ')': 'TK_CLOSE_PARENTH',
            '.': 'TK_DOT',
            ';': 'TK_SEMI_COLON',
            '+': 'TK_PLUS',
            '-': 'TK_MINUS',
            '/': 'TK_DIVIDE',
            '*': 'TK_MULTIPLY',
            '=': 'TK_EQUAL',
            ',': 'TK_COMMA',
            '>': 'TK_GREATER',
            '<': 'TK_LESS',
            ':=': 'TK_ASSIGNMENT'
        }
        self.TK_Characters = ['abcdefghijklmnoprqstuvwxyz']
        self.TK_Keywords = {}

        # Set up the Token Operators
        tk_keyword_setup(TK_Keywords)

    def tk_keyword_setup(keyword_dictionary):
        with open('keywords.txt', 'r') as keyword_file:
            for line in keyword_file:
                TK_Keywords[line] = 'TK_%s' % (line)
