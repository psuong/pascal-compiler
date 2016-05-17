import tokenizer
import byte_manager


class Error(Exception):
    pass


class ParserModule(object):
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token = None  # current_token is a tuple (TK_, value)
        self.instruction_pointer = 0
        self.data_pointer = 0
        self.symbol_table = []
        self.byte_array = bytearray(1000)  # For now allocate a large amount of memory

    def find_symbol_table_entry(self, name):
        """
        Looks through the entries in the symbol table and checks for the name. If it
        exists, return the instance of the symbol. Otherwise, return nothing.
        :param name: string
        :return: Symbol
        """
        for symbol in self.symbol_table:
            if symbol.name == name:
                return symbol
        return None

    def match_token(self, token_type):
        """
        Matches the current token with the token type.
        :param token_type: string
        :return: None
        """
        if self.current_token.tk_var == token_type:
            print 'Matched: %s, %s ' % (token_type, self.current_token.tk_var)
            try:
                # Get the next token list if available
                self.current_token = self.token_list.next()
            except StopIteration:
                return None
        else:
            raise Error('Token not found:\n Received: %s \n Got: %s' % (
                str(token_type),
                str(self.current_token.object_type)
            ))

    def generate_opcode(self, op_code):
        """
        Creates op_code and assigns it to the byte array. The instruction_pointer is
        additionally incremented by one.
        :param op_code:
        :return: None
        """
        self.byte_array[self.instruction_pointer] = op_code
        self.instruction_pointer += 1

    def generate_address(self, op_code):
        """
        Creates an address on four bytes and appends to a bytearray and increments the
        instruction_pointer by 4.
        :param op_code:
        :return:
        """
        for byte in bytearray(op_code):
            self.byte_array[self.instruction_pointer] = byte
            self.instruction_pointer += 1

    def parse(self):
        """
        Creates instructions in the byte_array
        :return:
        """
        self.current_token = self.token_list.next()
        # Match TK_KEYWORD_PROGRAM
        self.match_token('TK_KEYWORD_PROGRAM')
        self.match_token('TK_IDENTIFIER')
        self.match_token('TK_SEMI_COLON')
        # TODO: Check if the next token is a "VAR" token and perform
        # TODO: operations on it
        if self.current_token.tk_var == 'TK_VAR':
            pass
        else:
            # TODO: Otherwise start performing operations on the "BEGIN" keyword
            pass
        return self.byte_array

    def case_begin(self):
        self.match_token('TK_KEYWORD_BEGIN')
        # TODO Match the statements
        self.match_token('TK_KEYWORD_END')
        self.match_token('TK_EOF')
        # TODO: Generate the opcode
        self.match_token(byte_manager.op_code.HALT)

    def case_var(self):
        self.match_token('TK_VAR')
        var_declarations = []
        while self.current_token.tk_var == 'TK_ID':
            # If there exists a the variable int he var_declarations, then
            # the variable already exists. This is an error
            if self.current_token.tk_var in var_declarations:
                raise Error('Variable already declared: %s' % self.current_token.value)

            var_declarations.append(self.current_token.tk_var)
            self.match_token('TK_ID')

            # Multiple var declarations in the same line, check for
            # the commas.
            if self.current_token.tk_var == ',':
                self.match_token('TK_COMMA')
            self.match_token('TK_COLON')
            # TODO Check the datatypes of the variable declarations

    def case_pascal_statements(self):
        while self.current_token.object_type != 'TK_KEYWORD_END':
            object_type = self.current_token.object_type
            if object_type == 'TK_KEYWORD_WRITELN':
                # TODO: Add the writeln statement
                pass
            elif object_type == 'TK_KEYWORD_WHILE':
                pass
            elif object_type == 'TK_KEYWORD_REPEAT':
                pass
            elif object_type == 'TK_KEYWORD_IF':
                pass
            else:
                print 'Statements can\'t be matched.'
                return

    def write_line_statement(self):
        # Match the writeln keyword
        self.match_token('TK_KEYWORD_WRITELN')
        # Match the open_parenthesis
        self.match_token('TK_OPEN_PARENTH')
        while True:
            if self.current_token.object_type == 'TK_IDENTIFIER':
                symbol = self.find_entry_or_get_error()
                if symbol is None:
                    pass
            else:
                pass
        pass

    def find_entry_or_get_error(self):
        symbol = self.find_symbol_table_entry(self.current_token.value)
        pass
