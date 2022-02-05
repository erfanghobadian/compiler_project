from ply.lex import LexToken


class VariableDescriptor:
    sizes = {"REAL": 4, "REAL_NUMBER": 4, "INTEGER": 4, "INT": 4, "CHAR": 1, "BOOL": 1, "STRING": 4, "STRING_KEYWORD": 4}
    types = {
        'INTEGER': '.word',
        'INT': '.word',
        'REAL': '.word',
        'REAL_NUMBER': '.word',
        'CHAR': '.byte',
        'BOOL': '.byte',
        'STRING': '.asciiz',
        'STRING_KEYWORD': '.word'
    }

    def __init__(self, address, type, size=1):
        self.address = address

        self.type = type
        self.size = size

    def __len__(self):
        return VariableDescriptor.sizes[self.type] * self.size

    def __str__(self):
        return f"{self.address} {self.type} {self.size}"

    def __repr__(self):
        return str(self.__dict__)

    def get_asm_type(self):
        return self.types[self.type]


class MethodDescriptor:
    def __init__(self, return_type, start_code, param_list, address):
        self.address = address
        self.ar_size = 4
        self.param_address = 0
        self.return_type = return_type
        self.start_code = start_code
        self.param_list = param_list


class SymbolTable:
    def __init__(self):
        self.table = {}
        self.current_address = 0
        self.temp_index = 0
        self.parent = None
        self.name = None
        # current address in memory

    def find(self, name):
        parent = self
        while parent:
            if name in parent.table:
                return parent.table[name]
            parent = parent.parent
        return None

    def get_name_type(self, v_id):
        parent = self
        while parent:
            if v_id in parent.table:
                name = f"{parent.name}_{v_id}"
                v_type = parent.table[v_id].get_asm_type()
                return name, v_type
            parent = parent.parent
        return None

    def add_var(self, name, var_type, size):
        self.table[name] = VariableDescriptor(self.current_address, var_type, size)
        self.current_address += len(self.table[name])
        return self.table[name]

    def add_method(self, name, return_type, start_code, param_list):
        self.table[name] = MethodDescriptor(return_type, start_code, param_list, 0)
        return self.table[name]

    def get_temp(self, v_type, v_size=1):
        name = str(self.temp_index) + "temp"
        print(v_type)
        self.table[name] = VariableDescriptor(self.current_address, v_type, v_size)
        self.temp_index += 1
        self.current_address += len(self.table[name])
        token = LexToken()
        token.type = self.table[name].type
        token.lineno = 0
        token.lexpos = 0
        token.value = name
        return token
