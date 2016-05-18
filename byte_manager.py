class op_code:
    PUSHI = 0
    PUSH = 1
    POP = 2
    ADD = 3
    SUBTRACT = 4
    MULTIPLY = 5
    DIVIDE = 6
    DIV = 7
    GREATER_THAN = 8
    GREATER_THAN_EQ = 9
    EQUAL = 10
    NOT_EQUAL = 11
    DUP = 12
    JMP = 13
    JFALSE = 14
    JTRUE = 15
    HALT = 16
    PRINT = 17
    PRINT_I = 18
    PRINT_C = 19
    PRINT_B = 20
    PRINT_R = 21
    NEWLINE = 22
    NOT = 23
    FLOAT_ADD = 24
    FLOAT_SUBTRACT = 25
    FLOAT_MULTIPLY = 26
    FLOAT_DIVIDE = 27
    OR = 28
    PRINT_I_LIT = 29
    CVR = 30
    XCHG = 31

instruction_length = 5

conditionals = {
    '<': True,
    '<>': True,
    '<=': True,
    '>': True,
    '=': True
}


def byte_packer(value):
    """
    Performs bit manipulation to transform a value into to four bytes
    :param value: int
    :return: tuple
    """
    value = int(value)
    return (value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF


def byte_unpacker(byte_array):
    """
    Performs binary or operation and splices the byte array to the original value
    :param byte_array: list, tuple
    :return: int
    """
    return (byte_array[0] << 24) | (byte_array[1] << 16) | (byte_array[2] << 8) | (byte_array[3])


class Type(object):
    type_int, type_real, type_bool, type_char, type_string = range(5)
