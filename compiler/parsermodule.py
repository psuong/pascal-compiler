import tokenizer
import byte_manager
import symbol


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
        for symbol_entry in self.symbol_table:
            if symbol_entry.name == name:
                return symbol_entry
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
        if self.current_token.tk_var == 'TK_KEYWORD_VAR':
            self.case_var()
        else:
            # TODO: Otherwise start performing operations on the "BEGIN" keyword
            pass
        return self.byte_array

    def case_begin(self):
        self.match_token('TK_KEYWORD_BEGIN')
        self.statements()
        # self.match_token('TK_KEYWORD_END')
        # self.match_token('TK_EOF')
        # TODO: Generate the opcode
        # self.match_token(byte_manager.op_code.HALT)

    def statements(self):
        while self.current_token.tk_var != 'TK_EOF':
            type_of = self.current_token.tk_var
            if type_of == 'TK_IDENTIFIER':
                self.case_assignment()
            # TODO Check for TK_KEYWORD_WRITELN
            # TODO Check for TK_IDENTIFIER
            # TODO Check for TK_KEYWORD_WHILE
            # TODO Check for TK_KEYWORD_IF
            pass

    def case_var(self):
        self.match_token('TK_KEYWORD_VAR')
        var_declarations = []
        while self.current_token.tk_var == 'TK_IDENTIFIER':
            # If there exists a the variable int he var_declarations, then
            # the variable already exists. This is an error
            if self.current_token.tk_var in var_declarations:
                raise Error('Variable already declared: %s' % self.current_token.value)

            var_declarations.append(self.current_token)
            self.match_token('TK_IDENTIFIER')

            # Multiple var declarations in the same line, check for
            # the commas.
            if self.current_token.tk_var == ',':
                self.match_token('TK_COMMA')
            self.match_token('TK_COLON')
            # Case: integer datatype
        if self.current_token.tk_var == 'TK_DATATYPE_INTEGER':
            self.match_token('TK_DATATYPE_INTEGER')
        elif self.current_token.tk_var == 'TK_DATATYPE_REAL':
            self.match_token('TK_DATATYPE_REAL')
        elif self.current_token.tk_var == 'TK_DATATYPE_CHARACTER':
            self.match_token('TK_DATATYPE_CHARACTER')
        elif self.current_token.tk_var == 'TK_DATATYPE_BOOLEAN':
            self.match_token('TK_DATATYPE_BOOLEAN')
        else:
            raise Error('%s is an unknown data type' % self.current_token.tk_var)

        self.match_token('TK_SEMI_COLON')

        for each_var in var_declarations:
            self.symbol_table.append(symbol.Symbol(
                name=each_var.value,
                object_type=each_var.tk_var,
                data_type=symbol.VARIABLE
            ))
        if self.current_token.tk_var == 'TK_KEYWORD_VAR':
            self.case_var()
        else:
            self.case_begin()

    def case_pascal_statements(self):
        while self.current_token.object_type != 'TK_KEYWORD_END':
            object_type = self.current_token.object_type
            if object_type == 'TK_ID':
                pass
            elif object_type == 'TK_KEYWORD_WRITELN':
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

    def case_assignment(self):
        symbol_entry = self.find_entry_or_get_error()
        lhs_type = symbol_entry.data_type
        self.match_token('TK_IDENTIFIER')
        self.match_token('TK_ASSIGNMENT')
        rhs_type = self.expression()

        if lhs_type == rhs_type:
            self.generate_opcode(byte_manager.op_code.POP)
            self.generate_address(symbol_entry.data_pointer)
        else:
            raise Error('Type mismatch! %s does not equal %s!' % (lhs_type, rhs_type))

    def write_line_statement(self):
        # Match the writeln keyword
        self.match_token('TK_KEYWORD_WRITELN')
        # Match the open_parenthesis
        self.match_token('TK_OPEN_PARENTH')
        while True:
            # If reading a string literal
            if self.current_token.tk_var == 'TK_STRING_LIT':
                self.generate_opcode(byte_manager.op_code.PRINT)
            elif self.current_token.tk_var == 'TK_IDENTIFIER':
                symbol_entry = self.find_entry_or_get_error()
                # TODO Implement Expressions
                term = self.expression()
            else:
                pass
        pass

    def find_entry_or_get_error(self):
        symbol_entry = self.find_symbol_table_entry(self.current_token.value)
        if symbol_entry is None:
            raise Error('Variable %s is not declared' % self.current_token.value)
        else:
            return symbol_entry

    def expression(self):
        term = self.term()
        while self.current_token.tk_var == 'TK_OPERATOR_PLUS' or self.current_token.tk_var == 'TK_OPERATOR_MINUS':
            operator = self.current_token.tk_var
            self.match_token(operator)
            term2 = self.factor()
            term = self.emit(operator, term, term2)
        return term

    def term(self):
        term = self.factor()
        while self.current_token.tk_var == 'TK_OPERATOR' or self.current_token.tk_var == 'TK_DIVIDE':
            operator = self.current_token.tk_var
            self.match_token(operator)
            term2 = self.factor()
            term = self.emit(operator, term, term2)
        return term

    def factor(self):
        token_type = self.current_token.tk_var

        def generate_pushi_and_address(to_match):
            self.generate_opcode(byte_manager.op_code.PUSHI)
            self.generate_address(self.current_token.tk_var)
            self.match_token(to_match)
            return to_match

        if token_type == 'TK_IDENTIFIER':
            symbol_entry = self.find_entry_or_get_error()
            self.generate_opcode(byte_manager.op_code.PUSH)
            self.generate_address(symbol_entry.data_pointer)
            self.match_token('TK_IDENTIFIER')
            return symbol_entry.data_type
        elif token_type == 'TK_KEYWORD_NOT':
            self.generate_address(byte_manager.op_code.NOT)
            self.match_token('TK_KEYWORD_NOT')
            return self.factor()
        elif token_type == 'TK_OPEN_PARENTH':
            self.match_token('TK_OPEN_PARENTH')
            term1 = self.expression()
            self.match_token('TK_CLOSE_PARENTH')
            return term1
        elif token_type == 'TK_INTEGER':
            return generate_pushi_and_address('TK_INTEGER')
        elif token_type == 'TK_BOOLEAN':
            return generate_pushi_and_address('TK_BOOLEAN')
        elif token_type == 'TK_CHARACTER':
            return generate_pushi_and_address('TK_CHARACTER')
        elif token_type == 'TK_REAL':
            return generate_pushi_and_address('TK_REAL')

    def emit(self, operator, term1, term2):
        def boolean(operator, term1, term2):
            if term1 == term2:
                self.generate_opcode(operator)
            elif term1 == 'TK_INTEGER' and term2 == 'TK_REAL':
                self.generate_opcode(byte_manager.op_code.XCHG)
                self.generate_opcode(byte_manager.op_code.CVR)
                self.generate_opcode(byte_manager.op_code.XCHG)
                self.generate_opcode(operator)
            elif term1 == 'TK_REAL' and term2 == 'TK_INTEGER':
                self.generate_opcode(byte_manager.op_code.CVR)
                self.generate_opcode(operator)
            else:
                return None
            return 'TK_BOOLEAN'

        # Case: Adding two integers
        if operator == 'TK_OPERATOR_PLUS':
            if term1 == 'TK_INTEGER_LITERAL' and term2 == 'TK_INTEGER_LITERAL':
                self.generate_opcode(byte_manager.op_code.add)
                return 'TK_INTEGER'
