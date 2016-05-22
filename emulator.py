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
            print 'Instruction Pointer: 0%s \t | \tMatching: %s, %s' % (
                instruction_pointer, op_code_dict[operator], operator)
        else:
            print 'Instruction Pointer: %s \t | \tMatching: %s, %s' % (
                instruction_pointer, op_code_dict[operator], operator)

    def get_immediate_value(self):
        immediate_value = bytearray()
        for index in range(4):
            immediate_value.append(self.byte_array[self.instruction_pointer])
            self.instruction_pointer += 1
        value = byte_unpacker(immediate_value)
        return value

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
            self.push()
            self.execute()
        elif operator == OpCode.PRINT_I:
            self.print_i()
            self.execute()
        elif operator == OpCode.NEWLINE:
            self.print_newline()
            self.execute()
        elif operator == OpCode.PRINT_I_LIT:
            self.print_i()
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
        elif operator == OpCode.GREATER_THAN:
            self.greater_than()
            self.execute()
        elif operator == OpCode.GREATER_THAN_EQ:
            self.greater_than_equal()
            self.execute()
        elif operator == OpCode.LESS_THAN:
            self.less_than()
            self.execute()
        elif operator == OpCode.LESS_THAN_EQ:
            self.less_than_eq()
            self.execute()
        elif operator == OpCode.EQUAL:
            self.equal()
            self.execute()
        elif operator == OpCode.NOT_EQUAL:
            self.not_equal()
            self.execute()
        elif operator == OpCode.JFALSE:
            self.jump_false()
            self.execute()
        elif operator == OpCode.JMP:
            self.jump()
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

    def push(self):
        self.instruction_pointer += 1
        self.data_stack.append(self.get_immediate_data())

    def print_i(self):
        self.instruction_pointer += 1
        self.echo.append(self.get_immediate_data())

    def print_i_literal(self):
        self.instruction_pointer += 1
        value = self.get_immediate_value()
        self.echo.append(value)

    def print_r(self):
        self.instruction_pointer += 1
        self.echo.append(self.get_immediate_data())

    def print_newline(self):
        self.instruction_pointer += 1
        self.echo.append('\n')

    def add(self):
        self.instruction_pointer += 1
        lhs = self.data_stack.pop()
        rhs = self.data_stack.pop()
        self.data_stack.append(lhs + rhs)

    def subtract(self):
        self.instruction_pointer += 1
        rhs = self.data_stack.pop()
        lhs = self.data_stack.pop()
        self.data_stack.append(lhs - rhs)

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

    def greater_than(self):
        self.instruction_pointer += 1
        lhs = self.data_stack.pop()
        rhs = self.data_stack.pop()
        self.data_stack.append(rhs > lhs)

    def greater_than_equal(self):
        self.instruction_pointer += 1
        rhs = self.data_stack.pop()
        lhs = self.data_stack.pop()
        self.data_stack.append(lhs >= rhs)

    def jump_false(self):
        self.instruction_pointer += 1
        if self.data_stack.pop():
            self.get_immediate_value()
        else:
            value = self.get_immediate_value()
            self.instruction_pointer = value

    def jump(self):
        self.instruction_pointer += 1
        self.instruction_pointer = self.get_immediate_value()

    def less_than(self):
        self.instruction_pointer += 1
        rhs = self.data_stack.pop()
        lhs = self.data_stack.pop()
        self.data_stack.append(lhs < rhs)

    def less_than_eq(self):
        self.instruction_pointer += 1
        rhs = self.data_stack.pop()
        lhs = self.data_stack.pop()
        self.data_stack.append(lhs <= rhs)

    def equal(self):
        self.instruction_pointer += 1
        lhs = self.data_stack.pop()
        rhs = self.data_stack.pop()
        self.data_stack.append(lhs == rhs)

    def not_equal(self):
        self.instruction_pointer += 1
        lhs = self.data_stack.pop()
        rhs = self.data_stack.pop()
        self.data_stack.append(lhs != rhs)
