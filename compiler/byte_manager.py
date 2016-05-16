from aenum import Enum

op_code = Enum('OPCODE',
               'PUSHI PUSH POP ADD SUB MULTIPLY DIVIDE DIV CVR '
               'GTE DUP JMP JFALSE JTRUE HALT PRINT PRINT_I PRINT_C'
               'PRINT_B PRINT_R NEWLINE NOT XCHNG FADD FSUB FMULTIPLY'
               'OR LTE EQL NEQ GTR LES PRINT_I_LIT')

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
    # TODO: Unpack the byte array into the original value
    pass


class Type(object):
    type_int, type_real, type_bool, type_char, type_string = range(5)
