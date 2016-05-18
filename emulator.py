from parsermodule import Error, ParserModule
from byte_manager import op_code, byte_packer, byte_unpacker
import sys


class EmulatorModule(object):
    def __init__(self, byte_array):
        self.data_dict = {}
        self.data_stack = []
        self.byte_array = byte_array
        self.echo = []
        self.instruction_pointer = 0
        self.data_pointer = 0

    def echo_print_statements(self):
        print '============\nStandard Out\n============'
        for each in self.echo:
            print each

    def get_immediate_value(self):
        immediate_value = bytearray()
        for index in range(4):
            immediate_value.append(self.byte_array[self.instruction_pointer])
            self.instruction_pointer += 1
        return byte_unpacker(immediate_value)

    def get_immediate_data(self):
        """
        Takes the address and gets the data at the address.
        :return: bytearray
        """
        return self.data_dict[self.get_immediate_value()]

    def pop(self):
        self.instruction_pointer += 1
        popped = self.data_stack.pop()
        self.data_pointer = self.get_immediate_value()
        self.data_dict[self.data_pointer] = popped
        self.data_pointer += 1
        return popped

    def execute(self):
        operator = self.byte_array[self.instruction_pointer]
        print 'Instruction Pointer: %s' % self.instruction_pointer
        print 'Matching: %s' % operator

        if operator == op_code.PUSHI:
            self.push_i()
            self.execute()
        elif operator == op_code.POP:
            self.pop()
            self.execute()
        elif operator == op_code.PUSH:
            self.push_i()
            self.execute()
        elif operator == op_code.PRINT_I:
            self.print_i()
            self.execute()
        elif operator == op_code.HALT:
            sys.exit()
        else:
            print self.data_stack
            raise Error('%s not supported within the EmulatorModule!' % operator)

    def push_i(self):
        self.instruction_pointer += 1
        self.data_stack.append(self.get_immediate_value())

    def print_i(self):
        self.instruction_pointer += 1
        self.echo.append(self.get_immediate_data())

    def print_newline(self):
        self.instruction_pointer += 1
        self.echo.append('\n')

