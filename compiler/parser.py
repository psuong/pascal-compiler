class Parser(object):
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token = None
        self.instruction_pointer = 0
        self.data_pointer = 0
        self.symbol_table = []
        self.byte_array = bytearray(1000) # For now allocate a large amount of memory
