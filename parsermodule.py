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
        self.byte_array = bytearray(500)  # For now allocate a large amount of memory

    def find_symbol_table_entry(self, name):
        """
        Looks through the entries in the symbol table and checks for the name. If it
        exists, return the instance of the symbol. Otherwise, raise an error.
        :param name: string
        :return: Symbol
        """
        for symbol_entry in self.symbol_table:
            if symbol_entry.name == name:
                return symbol_entry
        raise Error('Variable [%s] is not found in the symbol table!' % name)

    def match_token(self, token_type):
        """
        Matches the current token with the token type.
        :param token_type: string
        :return: None
        """
        if self.current_token.token == token_type:
            print 'Matched: %s, %s ' % (token_type, self.current_token.value)
            try:
                # Get the next token list if available
                self.current_token = self.token_list.next()
            except StopIteration:
                return None
        else:
            raise Error('Token not found:\t Received: %s \t Got: %s' % (
                token_type,
                self.current_token.token
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
        instruction_pointer by 1.
        :param op_code:
        :return:
        """
        for byte in byte_manager.byte_packer(op_code):
            self.byte_array[self.instruction_pointer] = byte
            self.instruction_pointer += 1

    def generate_pushi_address(self, token_to_match):
        self.generate_opcode(byte_manager.OpCode.PUSHI)
        self.generate_address(self.current_token.value)
        self.match_token(token_to_match)
        return token_to_match

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
        if self.current_token.token == 'TK_KEYWORD_VAR':
            self.case_var()
        else:
            self.case_begin()
        return self.byte_array

    def case_begin(self):
        self.match_token('TK_KEYWORD_BEGIN')
        self.statements()
        # End statements of any kind of file.
        self.match_token('TK_KEYWORD_END')
        self.match_token('TK_DOT')
        self.match_token('TK_EOF')
        self.generate_opcode(byte_manager.OpCode.STOP)

    def statements(self):
        while self.current_token.token != 'TK_EOF':
            # print self.current_token.token
            token_type = self.current_token.token
            if token_type == 'TK_IDENTIFIER':
                self.case_assignment()
            elif token_type == 'TK_KEYWORD_WRITELN':
                self.case_writeln()
            elif token_type == 'TK_KEYWORD_IF':
                self.case_if()
            elif token_type == 'TK_KEYWORD_WHILE':
                self.case_while()
            elif token_type == 'TK_KEYWORD_FOR':
                self.case_for()
            elif token_type == 'TK_KEYWORD_REPEAT':
                self.case_repeat()
            elif token_type == 'TK_SEMI_COLON':
                self.match_token('TK_SEMI_COLON')
            # End case
            elif token_type == 'TK_KEYWORD_END':
                return
            else:
                return

    def case_var(self):
        self.match_token('TK_KEYWORD_VAR')
        var_declarations = []
        while self.current_token.token == 'TK_IDENTIFIER':
            # If there exists a the variable int he var_declarations, then
            # the variable already exists. This is an error
            if self.current_token.token in var_declarations:
                raise Error('Variable already declared: %s' % self.current_token.value)

            var_declarations.append(self.current_token)
            self.match_token('TK_IDENTIFIER')

            # Multiple var declarations in the same line, check for
            # the commas.
            if self.current_token.token == 'TK_COMMA':
                self.match_token('TK_COMMA')
            self.match_token('TK_COLON')

        if self.current_token.token == 'TK_DATATYPE_INTEGER':
            self.match_token('TK_DATATYPE_INTEGER')
            data_type = 'TK_DATATYPE_INTEGER'
        elif self.current_token.token == 'TK_DATATYPE_REAL':
            self.match_token('TK_DATATYPE_REAL')
            data_type = 'TK_DATATYPE_REAL'
        elif self.current_token.token == 'TK_DATATYPE_CHARACTER':
            self.match_token('TK_DATATYPE_CHARACTER')
            data_type = 'TK_DATATYPE_CHARACTER'
        elif self.current_token.token == 'TK_DATATYPE_BOOLEAN':
            self.match_token('TK_DATATYPE_BOOLEAN')
            data_type = 'TK_DATATYPE_BOOLEAN'
        elif self.current_token.token == 'TK_KEYWORD_ARRAY':
            self.match_token('TK_KEYWORD_ARRAY')
            data_type = 'TK_KEYWORD_ARRAY'
        else:
            raise Error('%s is an unknown data type' % self.current_token.token)

        if data_type == 'TK_KEYWORD_ARRAY':
            self.match_token('TK_LEFT_BRACKET')
            array_attributes = self.get_array_ranges(self.current_token)
            self.match_token('TK_RIGHT_BRACKET')
            self.match_token('TK_KEYWORD_OF')
            if self.current_token.token == 'TK_DATATYPE_INTEGER':
                self.match_token('TK_DATATYPE_INTEGER')
                assignment = 'TK_DATATYPE_INTEGER'
            else:
                raise Error('Type [%s] is not supported in arrays' % self.current_token.token)

            self.match_token('TK_SEMI_COLON')
            attributes = {
                'lhs': array_attributes['lhs'],
                'rhs': array_attributes['rhs'],
                'data_type': array_attributes['data_type'],
                'assignment': assignment
            }
            if array_attributes['data_type'] == 'TK_DATATYPE_INTEGER':
                for each_var in var_declarations:
                    self.symbol_table.append(symbol.Symbol(name=each_var.value,
                                                           object_type=symbol.ARRAY,
                                                           data_type='TK_DATATYPE_ARRAY',
                                                           data_pointer=self.data_pointer,
                                                           attribute=attributes))
                    self.data_pointer += 4 * int(array_attributes['rhs']) - int(array_attributes['lhs'])
            else:
                raise Error('Array access of %s is not supported' % attributes['data_type'])

        else:
            self.match_token('TK_SEMI_COLON')

            for each_var in var_declarations:
                self.symbol_table.append(symbol.Symbol(
                    name=each_var.value,
                    object_type=symbol.VARIABLE,
                    data_type=data_type,
                    data_pointer=self.data_pointer
                ))
                self.data_pointer += 1
        if self.current_token.token == 'TK_KEYWORD_VAR':
            self.case_var()
        else:
            self.case_begin()

    def get_array_ranges(self, token):
        self.match_token('TK_RANGE')
        data = {}
        list_of_ranges = token.value.split('..')
        if len(list_of_ranges) != 2:
            raise Error('The array range is off, the form is #..#, not %s' % token.value)
        lhs = list_of_ranges[0]
        rhs = list_of_ranges[1]

        if lhs.isdigit() and rhs.isdigit():
            lhs = int(lhs)
            rhs = int(rhs)
            data['data_type'] = 'TK_DATATYPE_INTEGER'
        data['lhs'] = lhs
        data['rhs'] = rhs
        data['token'] = token
        return data

    def case_writeln(self):
        self.match_token('TK_KEYWORD_WRITELN')
        self.match_token('TK_OPEN_PARENTH')
        while True:
            if self.current_token.token == 'TK_DATATYPE_STRING':
                self.generate_opcode(byte_manager.OpCode.PRINT_STRING_LIT)
                self.generate_address(self.current_token.value)
                self.match_token('TK_DATATYPE_STRING')
            elif self.current_token.token == 'TK_DATATYPE_CHARACTER':
                self.generate_opcode(byte_manager.OpCode.PRINT_C)
                self.generate_address(self.current_token.value)
                self.match_token('TK_DATATYPE_CHARACTER')
            elif self.current_token.token == 'TK_DATATYPE_INTEGER':
                self.generate_opcode(byte_manager.OpCode.PRINT_I_LIT)
                self.generate_address(int(self.current_token.value))
                self.match_token('TK_DATATYPE_INTEGER')
            elif self.current_token.token == 'TK_IDENTIFIER':
                symbol_entry = self.find_symbol_table_entry(self.current_token.value)
                term = self.expression()
                if term == 'TK_DATATYPE_INTEGER':
                    self.generate_opcode(byte_manager.OpCode.PRINT_I)
                    self.generate_address(symbol_entry.data_pointer)
                elif term == 'TK_DATATYPE_CHARACTER':
                    self.generate_opcode(byte_manager.OpCode.PRINT_C)
                    self.generate_address(symbol_entry.data_pointer)
                elif term == 'TK_DATATYPE_REAL':
                    self.generate_opcode(byte_manager.OpCode.PRINT_R)
                    self.generate_address(symbol_entry.data_pointer)
                else:
                    raise Error('%s is not supported within writeln!' % symbol_entry)
            else:
                raise Error('%s is not supported within writeln!' % self.current_token.value)

            if self.current_token.token == 'TK_COMMA':
                self.match_token('TK_COMMA')
            elif self.current_token.token == 'TK_CLOSE_PARENTH':
                self.match_token('TK_CLOSE_PARENTH')
                self.generate_opcode(byte_manager.OpCode.NEWLINE)
                return
            else:
                raise Error('Found %s, not comma or close parenthesis!' % self.current_token.value)

    def case_if(self):
        self.match_token('TK_KEYWORD_IF')
        self.conditional_statement()
        self.match_token('TK_KEYWORD_THEN')
        self.generate_opcode(byte_manager.OpCode.JFALSE)
        hole = self.instruction_pointer
        self.generate_address(0)
        self.statements()
        if self.current_token.token == 'TK_KEYWORD_ELSE':
            self.generate_opcode(byte_manager.OpCode.JMP)
            hole_2 = self.instruction_pointer
            self.generate_address(0)
            save = self.instruction_pointer
            self.instruction_pointer = hole
            self.generate_address(save)
            self.instruction_pointer = save
            hole = hole_2
            self.match_token('TK_KEYWORD_ELSE')
            self.statements()
        save = self.instruction_pointer
        self.instruction_pointer = hole
        self.generate_address(save)
        self.instruction_pointer = save

    def case_while(self):
        self.match_token('TK_KEYWORD_WHILE')
        entry = self.instruction_pointer
        self.conditional_statement()
        self.match_token('TK_KEYWORD_DO')
        self.generate_opcode(byte_manager.OpCode.JFALSE)
        hole = self.instruction_pointer
        self.generate_address(0)
        self.match_token('TK_KEYWORD_BEGIN')
        self.statements()
        self.match_token('TK_KEYWORD_END')
        self.match_token('TK_SEMI_COLON')
        self.generate_opcode(byte_manager.OpCode.JMP)
        self.generate_address(entry)
        save = self.instruction_pointer
        self.instruction_pointer = hole
        self.generate_address(save)
        self.instruction_pointer = save

    def case_for(self):
        self.match_token('TK_KEYWORD_FOR')
        value = self.current_token.value
        self.case_assignment()
        entry = self.instruction_pointer
        symbol_entry = self.find_symbol_table_entry(value)

        if self.current_token.token == 'TK_KEYWORD_TO':
            self.match_token('TK_KEYWORD_TO')
            self.generate_opcode(byte_manager.OpCode.PUSH)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.PUSHI)
            self.generate_address(self.current_token.value)
            self.generate_opcode(byte_manager.OpCode.LESS_THAN_EQ)
            self.match_token('TK_DATATYPE_INTEGER')
            self.match_token('TK_KEYWORD_DO')
            self.generate_opcode(byte_manager.OpCode.JFALSE)
            hole = self.instruction_pointer
            self.generate_address(0)

            self.match_token('TK_KEYWORD_BEGIN')
            self.statements()
            self.match_token('TK_KEYWORD_END')
            self.match_token('TK_SEMI_COLON')

            self.generate_opcode(byte_manager.OpCode.PUSH)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.PUSHI)
            self.generate_address(1)
            self.generate_opcode(byte_manager.OpCode.ADD)
            self.generate_opcode(byte_manager.OpCode.POP)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.JMP)
            self.generate_address(entry)
            save = self.instruction_pointer
            self.instruction_pointer = hole
            self.generate_address(save)
            self.instruction_pointer = save

        elif self.current_token.token == 'TK_KEYWORD_DOWNTO':
            self.match_token('TK_KEYWORD_DOWNTO')
            self.generate_opcode(byte_manager.OpCode.PUSH)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.PUSHI)
            self.generate_address(self.current_token.value)
            self.generate_opcode(byte_manager.OpCode.GREATER_THAN_EQ)
            self.match_token('TK_DATATYPE_INTEGER')
            self.match_token('TK_KEYWORD_DO')
            self.generate_opcode(byte_manager.OpCode.JFALSE)
            hole = self.instruction_pointer
            self.generate_address(0)

            self.match_token('TK_KEYWORD_BEGIN')
            self.statements()
            self.match_token('TK_KEYWORD_END')
            self.match_token('TK_SEMI_COLON')

            self.generate_opcode(byte_manager.OpCode.PUSH)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.PUSHI)
            self.generate_address(1)
            self.generate_opcode(byte_manager.OpCode.SUBTRACT)
            self.generate_opcode(byte_manager.OpCode.POP)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.JMP)
            self.generate_address(entry)
            save = self.instruction_pointer
            self.instruction_pointer = hole
            self.generate_address(save)
            self.instruction_pointer = save

    def case_repeat(self):
        self.match_token('TK_KEYWORD_REPEAT')
        entry = self.instruction_pointer
        self.statements()
        self.match_token('TK_KEYWORD_UNTIL')
        self.conditional_statement()
        self.generate_opcode(byte_manager.OpCode.JFALSE)
        self.generate_address(entry)

    def case_assignment(self):
        symbol_entry = self.find_symbol_table_entry(self.current_token.value)
        left_hand_side = symbol_entry.data_type
        self.match_token('TK_IDENTIFIER')
        if self.current_token.token == 'TK_LEFT_BRACKET':
            self.assign_array(symbol_entry)
            return
        self.match_token('TK_ASSIGNMENT')
        right_hand_side = self.expression()
        if left_hand_side == right_hand_side:
            self.generate_opcode(byte_manager.OpCode.POP)
            self.generate_address(symbol_entry.data_pointer)
        else:
            raise Error('Mismatched %s is not equal to %s!' % (left_hand_side, right_hand_side))

    def term(self):
        term = self.factor()
        while self.current_token.token == 'TK_MULTIPLY' or self.current_token.token == 'TK_DIVIDE' or self.current_token.token == 'TK_KEYWORD_DIV':
            operator = self.current_token.token
            self.match_token(self.current_token.token)
            term_1 = self.factor()
            term = self.emit(operator, term, term_1)
        return term

    def expression(self):
        term = self.term()
        while self.current_token.token == 'TK_PLUS' or self.current_token.token == 'TK_MINUS':
            operator = self.current_token.token
            self.match_token(operator)
            term_1 = self.term()
            term = self.emit(operator, term, term_1)
        return term

    def factor(self):
        token = self.current_token.token
        if token == 'TK_IDENTIFIER':
            symbol_entry = self.find_symbol_table_entry(self.current_token.value)
            if symbol_entry.object_type == symbol.VARIABLE:
                self.generate_opcode(byte_manager.OpCode.PUSH)
                self.generate_address(symbol_entry.data_pointer)
                self.match_token('TK_IDENTIFIER')
                return symbol_entry.data_type
            elif symbol_entry.object_type == symbol.ARRAY:
                self.match_token('TK_IDENTIFIER')
                self.access_array(symbol_entry)
                self.generate_opcode(byte_manager.OpCode.GET)
                return symbol_entry.data_type
        elif token == 'TK_KEYWORD_NOT':
            self.generate_address(byte_manager.OpCode.NOT)
            self.match_token('TK_KEYWORD_NOT')
            return self.factor()
        elif token == 'TK_OPEN_PARENTH':
            self.match_token('TK_OPEN_PARENTH')
            term = self.expression()
            self.match_token('TK_CLOSE_PARENTH')
            return term

        # Case Data types
        elif token == 'TK_DATATYPE_INTEGER':
            return self.generate_pushi_address('TK_DATATYPE_INTEGER')
        elif token == 'TK_DATATYPE_REAL':
            return self.generate_pushi_address('TK_DATATYPE_REAL')
        elif token == 'TK_DATATYPE_BOOLEAN':
            return self.generate_pushi_address('TK_DATATYPE_BOOLEAN')
        elif token == 'TK_DATATYPE_CHARACTER':
            return self.generate_pushi_address('TK_DATATYPE_CHARACTER')

    def emit(self, operator, term_1, term_2):
        if operator == 'TK_PLUS':
            return self.case_emit_plus(term_1, term_2)
        elif operator == 'TK_MINUS':
            return self.case_emit_minus(term_1, term_2)
        elif operator == 'TK_MULTIPLY':
            return self.case_emit_multiply(term_1, term_2)
        elif operator == 'TK_DIVIDE':
            return self.case_emit_divide(term_1, term_2)
        elif operator == 'TK_KEYWORD_DIV':
            self.generate_opcode(byte_manager.OpCode.DIVIDE)
            return 'TK_DATATYPE_INTEGER'
        elif operator == 'TK_KEYWORD_OR':
            return self.case_emit_or(term_1, term_2)
        elif operator == 'TK_GREATER_EQ':
            return self.compare_terms(byte_manager.OpCode.GREATER_THAN_EQ, term_1, term_2)
        elif operator == 'TK_GREATER':
            return self.compare_terms(byte_manager.OpCode.GREATER_THAN, term_1, term_2)
        elif operator == 'TK_LESS_EQ':
            return self.compare_terms(byte_manager.OpCode.LESS_THAN_EQ, term_1, term_2)
        elif operator == 'TK_LESS':
            return self.compare_terms(byte_manager.OpCode.LESS_THAN, term_1, term_2)
        elif operator == 'TK_EQUAL':
            return self.compare_terms(byte_manager.OpCode.EQUAL, term_1, term_2)
        elif operator == 'TK_NOT_EQUAL':
            return self.compare_terms(byte_manager.OpCode.NOT_EQUAL, term_1, term_2)
        else:
            raise Error('Emit could not match operator: %s' % operator)

    def compare_terms(self, operator, term_1, term_2):
        if term_1 == term_2:
            self.generate_opcode(operator)
        elif term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(operator)
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(operator)
        else:
            return None
        return 'TK_DATATYPE_BOOL'

    def case_emit_plus(self, term_1, term_2):
        if term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.ADD)
            return 'TK_DATATYPE_INTEGER'
        elif term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.FLOAT_ADD)
            return 'TK_DATATYPE_REAL'
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.FLOAT_ADD)
            return 'TK_DATATYPE_REAL'
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.FLOAT_ADD)
            return 'TK_DATATYPE_REAL'
        return None

    def case_emit_minus(self, term_1, term_2):
        if term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.SUBTRACT)
            return 'TK_DATATYPE_INTEGER'
        elif term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.FLOAT_SUBTRACT)
            return 'TK_DATATYPE_REAL'
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.FLOAT_SUBTRACT)
            return 'TK_DATATYPE_REAL'
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.FLOAT_SUBTRACT)
            return 'TK_DATATYPE_REAL'
        return None

    def case_emit_multiply(self, term_1, term_2):
        if term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.MULTIPLY)
            return 'TK_DATATYPE_INTEGER'
        elif term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.FLOAT_MULTIPLY)
            return 'TK_DATATYPE_REAL'
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.FLOAT_MULTIPLY)
            return 'TK_DATATYPE_REAL'
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.FLOAT_MULTIPLY)
            return 'TK_DATATYPE_REAL'
        return None

    def case_emit_divide(self, term_1, term_2):
        if term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.DIVIDE)
        elif term_1 == 'TK_DATATYPE_INTEGER' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.DIVIDE)
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_INTEGER':
            self.generate_opcode(byte_manager.OpCode.CVR)
            self.generate_opcode(byte_manager.OpCode.DIVIDE)
        elif term_1 == 'TK_DATATYPE_REAL' and term_2 == 'TK_DATATYPE_REAL':
            self.generate_opcode(byte_manager.OpCode.DIVIDE)
        return 'TK_DATATYPE_REAL'

    def case_emit_or(self, term_1, term_2):
        if term_1 == 'TK_DATATYPE_BOOLEAN' and term_2 == 'TK_DATATYPE_BOOLEAN':
            self.generate_opcode(byte_manager.OpCode.OR)
            return 'TK_DATATYPE_BOOLEAN'
        return None

    def conditional_statement(self):
        term = self.expression()
        conditional_operator = self.current_token.value
        if byte_manager.conditionals.get(conditional_operator) is None:
            raise Error('Conditional operator, [%s], not found!' % conditional_operator)
        else:
            token = self.current_token.token
            self.match_token(token)
            term_1 = self.term()
            term = self.emit(token, term, term_1)
        return term

    def access_array(self, symbol_entry):
        self.match_token('TK_LEFT_BRACKET')
        current_symbol = self.find_symbol_table_entry(self.current_token.value)
        self.generate_opcode(byte_manager.OpCode.PUSH)
        self.generate_address(current_symbol.data_pointer)
        self.match_token('TK_IDENTIFIER')
        self.match_token('TK_RIGHT_BRACKET')

        self.generate_opcode(byte_manager.OpCode.PUSHI)

        if current_symbol.data_type == 'TK_DATATYPE_INTEGER':
            self.generate_address(symbol_entry.lhs)
            self.generate_opcode(byte_manager.OpCode.XCHG)
            self.generate_opcode(byte_manager.OpCode.SUBTRACT)
            self.generate_opcode(byte_manager.OpCode.PUSHI)
            self.generate_address(4)
            self.generate_opcode(byte_manager.OpCode.MULTIPLY)
            self.generate_opcode(byte_manager.OpCode.PUSHI)
            self.generate_address(symbol_entry.data_pointer)
            self.generate_opcode(byte_manager.OpCode.ADD)
        else:
            raise Error('Datatype %s, not supported in arrays yet' % current_symbol.data_type)

    def assign_array(self, symbol_entry):
        self.access_array(symbol_entry)
        self.match_token('TK_ASSIGNMENT')
        expression = self.expression()
        if expression == symbol_entry.data_type:
            self.generate_opcode(byte_manager.OpCode.DUMP_VALUES)
        else:
            raise Error('Mismatch in array assignment with %s and %s.' % (expression, symbol_entry.data_type))
