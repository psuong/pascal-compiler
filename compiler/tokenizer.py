def tk_keyword_setup():
        """
        Generates a dictionary of keywords found in Pascal.

        :return: dictionary
        """
        keyword_dict = {}
        with open('compiler/keywords.txt', 'r') as keyword_file:
            for line in keyword_file:
                keyword_dict[line.rstrip()] = 'TK_%s' % (line.upper().rstrip())
        return keyword_dict


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
        self.TK_Keywords = None
        self.TK_File = {
            'EOF': 'TK_EOF'
        }
