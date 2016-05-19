from parsermodule import Error, ParserModule
from byte_manager import OpCode, byte_packer, byte_unpacker, op_code_dict
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

    def print_instruction(self, instruction_pointer, operator):
        if instruction_pointer < 10:
            print 'Instruction Pointer: 0%s \t | \tMatching: %s' % (instruction_pointer, op_code_dict[operator])
        else:
            print 'Instruction Pointer: %s \t | \tMatching: %s' % (instruction_pointer, op_code_dict[operator])

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
        self.print_instruction(self.instruction_pointer, operator)

        if operator == OpCode.PUSHI:
            self.push_i()
            self.execute()
        elif operator == OpCode.POP:
            self.pop()
            self.execute()
        elif operator == OpCode.PUSH:
            self.push_i()
            self.execute()
        elif operator == OpCode.PRINT_I:
            self.print_i()
            self.execute()
        elif operator == OpCode.NEWLINE:
            self.print_newline()
            self.execute()
        elif operator == OpCode.ADD:
            self.add()
            self.execute()
        elif operator == OpCode.SUBTRACT:
            self.subtract()
            self.execute()
        elif operator == OpCode.FLOAT_ADD:
            self.add()
            self.execute()
        elif operator == OpCode.FLOAT_SUBTRACT:
            self.subtract()
            self.execute()
        elif operator == OpCode.MULTIPLY:
            self.multiply()
            self.execute()
        elif operator == OpCode.DIV:
            self.divide()
            self.execute()
        elif operator == OpCode.DIVIDE:
            self.divide()
            self.execute()
        elif operator == OpCode.CVR:
            self.convert_cvr()
            self.execute()
        elif operator == OpCode.XCHG:
            self.exchange_xchg()
            self.execute()
        elif operator == OpCode.PRINT_R:
            self.print_r()
            self.execute()
        elif operator == OpCode.STOP:
            self.echo_print_statements()
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

    def print_r(self):
        self.instruction_pointer += 1
        self.echo.append(self.get_immediate_data())

    def print_newline(self):
        self.instruction_pointer += 1
        self.echo.append('\n')

    def add(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side + right_hand_side)

    def subtract(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(right_hand_side - left_hand_side)

    def multiply(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(right_hand_side * left_hand_side)

    def divide(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(right_hand_side / left_hand_side)

    def convert_cvr(self):
        self.instruction_pointer += 1
        popped = self.data_stack.pop()
        self.data_stack.append(float(popped))

    def exchange_xchg(self):
        self.instruction_pointer += 1
        top = self.data_stack.pop()
        bottom = self.data_stack.pop()
        self.data_stack.append(top)
        self.data_stack.append(bottom)
