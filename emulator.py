from parsermodule import Error, ParserModule
from byte_manager import op_code, byte_packer, byte_unpacker
import sys


class EmulatorModule(object):
    def __init__(self, byte_array):
        self.data_array = []
        self.data_stack = []
        self.byte_array = byte_array
        self.echo = []
        self.instruction_pointer = 0
        self.data_pointer = 0

    def echo_print_statements(self):
        print '============nStandard Out\n============'
        for each in self.echo:
            print each

    def execute(self):
        print 'Instruction Pointer: %s' % self.instruction_pointer
        operator = self.byte_array[self.instruction_pointer]

        print operator

        if operator == op_code.PUSHI:
            self.push_and_push_i()
            self.execute()
        elif operator == op_code.POP:
            self.pop_item()
            self.execute()
        elif operator == op_code.PUSH:
            self.push_and_push_i()
            self.execute()
        elif operator == op_code.PRINT_I:
            self.print_i()
            self.execute()
        elif operator == op_code.PRINT_I_LIT:
            self.print_i_lit()
            self.execute()
        elif operator == op_code.PRINT_C:
            self.print_char()
            self.execute()
        elif operator == op_code.NEWLINE:
            self.print_newline()
            self.execute()
        elif operator == op_code.ADD:
            self.add()
            self.execute()
        elif operator == op_code.SUBTRACT:
            self.subtract()
            self.execute()
        elif operator == op_code.JFALSE:
            self.jump_false()
            self.execute()
        elif operator == op_code.GREATER_THAN_EQ:
            self.greater_than_eq()
            self.execute()
        elif operator == op_code.LESS_THAN_EQ:
            self.less_than_eq()
            self.execute()
        elif operator == op_code.LESS_THAN:
            self.less_than()
            self.execute()
        elif operator == op_code.GREATER_THAN:
            self.greater_than()
            self.execute()
        elif operator == op_code.EQUAL:
            self.equal()
            self.execute()
        elif operator == op_code.NOT_EQUAL:
            self.not_equal()
            self.execute()
        elif operator == op_code.XCHG:
            self.exchange_xchg()
            self.execute()
        elif operator == op_code.CVR:
            self.convert_cvr()
            self.execute()
        elif operator == op_code.JMP:
            self.jump()
            self.execute()
        elif operator == op_code.POP_CHAR:
            self.pop_char()
            self.execute()
        elif operator == op_code.MULTIPLY:
            self.multiply()
            self.execute()
        elif operator == op_code.HALT:
            print 'Finished simulating program.'
            self.echo_print_statements()
            sys.exit()
        elif operator == op_code.PUSH_CHAR:
            self.push_char()
            self.execute()
        elif operator == op_code.DIVIDE:
            self.divide()
            self.execute()
        else:
            print 'Stack', self.data_stack
            raise Error('Emulator lacks support for opcode %i' % operator)

    def push_and_push_i(self):
        self.instruction_pointer += 1
        self.data_stack.append(self.get_unpacked_immediate_value())

    def pop_item(self):
        self.instruction_pointer += 1
        popped = self.data_stack.pop()
        self.data_pointer = self.get_unpacked_immediate_value()
        self.data_array[self.data_pointer] = popped
        self.data_pointer += 1
        return popped

    def print_i(self):
        self.instruction_pointer += 1
        self.echo.append(self.get_unpacked_immediate_value())

    def print_i_lit(self):
        self.instruction_pointer += 1
        value = self.get_unpacked_immediate_value()
        self.echo.append(value)

    def print_newline(self):
        self.instruction_pointer += 1
        self.echo.append('\n')

    def subtract(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side - right_hand_side)

    def add(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side + right_hand_side)

    def greater_than_eq(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side >= right_hand_side)

    def greater_than(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side > right_hand_side)

    def less_than_eq(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side <= right_hand_side)

    def less_than(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side < right_hand_side)

    def equal(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side == right_hand_side)

    def not_equal(self):
        self.instruction_pointer += 1
        left_hand_side = self.data_stack.pop()
        right_hand_side = self.data_stack.pop()
        self.data_stack.append(left_hand_side != right_hand_side)

    def convert_cvr(self):
        self.instruction_pointer += 1
        self.data_stack.append(float(self.data_stack.pop()))

    def exchange_xchg(self):
        self.instruction_pointer += 1
        top = self.data_stack.pop()
        bottom = self.data_stack.pop()
        self.data_stack.append(top)
        self.data_stack.append(bottom)

    def jump(self):
        self.instruction_pointer += 1
        self.instruction_pointer = self.get_unpacked_immediate_value()

    def jump_false(self):
        self.instruction_pointer += 1
        if self.data_stack.pop():
            self.get_unpacked_immediate_value()
        else:
            immediate_value = self.get_unpacked_immediate_value()
            print 'Jumped to: %s', immediate_value
            self.instruction_pointer = immediate_value

    def get_unpacked_immediate_value(self):
        value = bytearray()
        for index in range(0, 4):
            value.append(self.byte_array[self.instruction_pointer])
            self.instruction_pointer += 1
        return byte_unpacker(value)

    def pop_char(self):
        self.instruction_pointer += 1
        popped = self.data_stack.pop()
        self.data_pointer = self.get_unpacked_immediate_value()
        self.data_array[self.data_pointer] = chr(popped)
        self.data_pointer += 1
        return popped

    def push_char(self):
        self.instruction_pointer += 1
        self.data_stack.append(self.get_unpacked_immediate_value())

    def multiply(self):
        self.instruction_pointer += 1
        self.data_stack.append(self.get_unpacked_immediate_value())

    def divide(self):
        self.instruction_pointer += 1
        denominator = self.data_stack.pop()
        self.data_stack.append(self.data_stack.pop() / denominator)

    def print_char(self):
        self.instruction_pointer += 1
        self.echo.append(self.data_array[self.get_unpacked_immediate_value()])
