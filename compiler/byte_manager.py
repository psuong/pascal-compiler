from aenum import Enum

op_code = Enum('OPCODE',
               'PUSHI PUSH POP ADD SUB MULTIPLY DIVIDE DIV CVR '
               'GTE DUP JMP JFALSE JTRUE HALT PRINT PRINT_I PRINT_C'
               'PRINT_B PRINT_R NEWLINE NOT XCHNG FADD FSUB FMULTIPLY'
               'OR LTE EQL NEQ GTR LES PRINT_I_LIT')


instruction_length = 5


class Type(object):
    type_int, type_real, type_bool, type_char, type_string = range(5)