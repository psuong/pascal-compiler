class Token:
    def tk_keyword_setup():
        """
        Generates a dictionary of keywords found in Pascal.

        :return: dictionary
        """
        keyword_dict = {}
        with open('keywords.txt', 'r') as keyword_file:
            for line in keyword_file:
                keyword_dict[line] = 'TK_%s' % (line)
        return keyword_dict

    def __init__(self):
        def tk_keyword_setup():
            keyword_dict = {}
            with open('keywords.txt', 'r') as keyword_file:
                for line in keyword_file:
                    keyword_dict[line] = 'TK_%s' % (line)
            return keyword_dict

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
        self.TK_Keywords = tk_keyword_setup()
