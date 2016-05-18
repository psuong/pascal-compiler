from aenum import Enum

op_code = Enum('OPCODE',
               'PUSHI PUSH POP ADD SUBTRACT MULTIPLY DIVIDE DIV CVR'
               'GREATER_THAN_EQ GREATER_THAN'
               'LESS_THAN_EQ LESS_THAN'
               'EQUAL NOT_EQUAL'
               'DUP JMP JFALSE JTRUE HALT PRINT PRINT_I PRINT_C'
               'PRINT_B PRINT_R NEWLINE NOT XCHG'
               'FLOAT_ADD FLOAT_SUBTRACT FLOAT_MULTIPLY FLOAT_DIVIDE'
               'OR PRINT_I_LIT')

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
