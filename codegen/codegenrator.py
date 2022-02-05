from ._helpers import *
from .sym_table import SymbolTable, VariableDescriptor


class CodeGenerator:

    def __init__(self):
        self.sem_stack = []
        self.sym_table = None
        self.code = []
        self.data = []
        self.pc = 0

    def generate_code(self, opcode, operand):
        if opcode == "NoSem":
            return
        try:
            print("{} {}".format(opcode, operand))
            for opc in opcode.split('&'):
                getattr(self, "handle_" + opc.replace('@', ''))(operand)
        except Exception as e:
            print(e.with_traceback())
            pass

    def new_scope(self, name):
        st = SymbolTable()
        if self.sym_table:
            st.name = f"{self.sym_table.name}_{name}"
            st.parent = self.sym_table
        else:
            st.name = name
        self.sym_table = st

    def add_var(self, var_id, value=0):
        name, v_type = self.sym_table.get_name_type(var_id)
        print(v_type)
        if v_type == '.asciiz':
            if not value:
                value = "\"\""
            self.data.append(f"{name}: {v_type}, {value}\n")
        else:
            self.data.append(f"{name}: {v_type}, {value}\n")

    def close_scope(self):
        self.sym_table = self.sym_table.parent

    def handle_push(self, operand):
        self.sem_stack.append(operand)

    def handle_declare_var(self, operand):
        if operand.type != 'ID':
            print("FUCK")
            return
        var_id = operand.value
        var_type = self.sem_stack[-1]
        self.sym_table.add_var(var_id, var_type.type, 1)
        self.add_var(var_id)

        print(self.sym_table.table)

    def handle_pop(self, operand):
        self.sem_stack.pop()

    def handle_declare_arr(self, operand):
        var_id = operand.value
        var_type = self.sem_stack[-1]
        self.sym_table.add_var(var_id, var_type.type, None)
        print(self.sym_table.table)

    def handle_declare_method_void(self, operand):
        m_id = self.sem_stack[-1]
        if self.sym_table.find(m_id) is not None:
            raise Exception(f"function {operand} already defined")
        self.sym_table.add_method(m_id, 'void', self.pc, dict())
        self.new_scope(name=m_id)

    def handle_declare_method_non_void(self, operand):
        m_id = operand.value
        m_type = self.sem_stack.pop()
        if self.sym_table.find(m_id) is not None:
            raise Exception(f"function {m_id} already defined")
        self.sem_stack.append(m_id)
        func_desc = self.sym_table.add_method(m_id, m_type.value, self.pc, dict())
        # func_desc.ar_size += VariableDescriptor.sizes.get(m_type.value)
        self.new_scope(name=m_id)

    def handle_declare_method_param(self):
        m_id = self.sem_stack.pop()
        m_type = self.sem_stack.pop()
        m_func_id = self.sem_stack[-1]
        m_func_desc = self.sym_table.find(m_func_id)
        if m_id in m_func_desc.param_list:
            raise Exception(f"parameter {m_id} already defined")
        m_func_desc.param_list[m_id] = VariableDescriptor(m_func_desc.param_address, type)
        m_func_desc.param_address += VariableDescriptor.sizes[m_type]
        m_func_desc.ar_size += VariableDescriptor.sizes[m_type]
        m_func_desc.ar_size += VariableDescriptor.sizes[m_type]

    def handle_declare_method_end(self, operand):
        print(self.sym_table.table)
        self.close_scope()
        m_id = self.sem_stack.pop()
        # func_desc = self.sym_table.find(m_id)
        # print(func_desc)
        # for var in self.sym_table.table:
        #     func_desc.ar_size += len(self.sym_table.table[var])

    def handle_declare_class(self, operand):
        c_id = operand.value
        print(c_id)
        self.new_scope(name=c_id)

    def handle_end_declare_class(self, operand):
        pass

    def handle_assignment(self, operand):
        print(self.sem_stack)
        r_value = self.sem_stack.pop()
        if r_value == 'noass':
            return
        assignment = self.sem_stack.pop()
        l_value = self.sem_stack.pop()
        if l_value.type == 'ID':
            l_var_desc = self.sym_table.find(l_value.value)
            if l_var_desc is None:
                raise Exception(f"variable {l_value.value} not defined")
            check_type_mismatch(l_var_desc.type, r_value.type)
            if r_value.type in ['INTEGER', 'REAL_NUMBER']:
                code = f"li $t0, {r_value.value}\n"
                self.add_code(code)
            elif r_value.type == 'STRING':
                tmp = self.sym_table.get_temp('STRING')
                self.add_var(tmp.value, value=r_value.value)
                name, _ = self.sym_table.get_name_type(tmp.value)
                code = f"la $t0, {name}\n"
                self.add_code(code)
            elif r_value.type == 'BOOLEAN':
                code = f"li $t0, {r_value.value}\n"
                self.add_code(code)
            else:
                name, v_type = self.sym_table.get_name_type(r_value.value)
                code = f"l{type_asm_map[v_type]} $t0, {name}\n"
                self.add_code(code)
            name, v_type = self.sym_table.get_name_type(l_value.value)

            code = f"s{'w' if v_type == '.asciiz' else type_asm_map[v_type]} $t0, {name}\n"
            self.add_code(code)

    def handle_assignment_for(self, operand):
        self.handle_assignment(operand)
        self.sem_stack.append(self.pc)

    def handle_add_minus(self, operand):
        print(self.sem_stack)
        opr2 = self.sem_stack.pop()
        operation = self.sem_stack.pop()
        opr1 = self.sem_stack.pop()
        if opr1.type == 'ID':
            opr1_desc = self.sym_table.find(opr1.value)
            if opr1_desc is None:
                raise Exception(f"variable {opr1.value} not defined")
            opr1.type = opr1_desc.type
        tmp = self.sym_table.get_temp(math_op_output_type(operation.value, opr1.type, opr2.type))
        self.add_var(tmp.value)
        self.sem_stack.append(tmp)
        for reg, op in zip(['$t0', '$t1'], [opr1, opr2]):
            if op.type in ['INTEGER', 'REAL_NUMBER']:
                code = f"li {reg}, {op.value}\n"
                self.add_code(code)
            else:
                name, v_type = self.sym_table.get_name_type(op.value)
                code = f"l{type_asm_map[v_type]} {reg}, {name}\n"
                self.add_code(code)
        code = f"{operation_map[operation.value]} $t2, $t0, $t1\n"
        self.add_code(code)
        tmp_name, v_type = self.sym_table.get_name_type(tmp.value)
        code = f"s{type_asm_map[v_type]} $t2, {tmp_name}\n"
        self.add_code(code)

        print(self.sem_stack)

    def handle_times_divide_and(self, operand):
        print(self.sem_stack)
        opr2 = self.sem_stack.pop()
        operation = self.sem_stack.pop()
        opr1 = self.sem_stack.pop()
        if opr1.type == 'ID':
            opr1_desc = self.sym_table.find(opr1.value)
            if opr1_desc is None:
                raise Exception(f"variable {opr1.value} not defined")
            opr1.type = opr1_desc.type
        if opr2.type == 'ID':
            opr2_desc = self.sym_table.find(opr2.value)
            if opr2_desc is None:
                raise Exception(f"variable {opr2.value} not defined")
            opr2.type = opr2_desc.type
        tmp = self.sym_table.get_temp(math_op_output_type(operation.value, opr1.type, opr2.type))
        self.add_var(tmp.value)
        self.sem_stack.append(tmp)
        for reg, op in zip(['$t0', '$t1'], [opr1, opr2]):
            if op.type in ['INTEGER', 'REAL_NUMBER']:
                code = f"li {reg}, {op.value}\n"
                self.add_code(code)
            else:
                name, _ = self.sym_table.get_name_type(op.value)
                code = f"lw {reg}, {name}\n"
                self.add_code(code)
        print(operation_map[operation.value])
        code = f"{operation_map[operation.value]} $t2, $t0, $t1\n"
        self.add_code(code)
        tmp_name, _ = self.sym_table.get_name_type(tmp.value)
        code = f"sw $t2, {tmp_name}\n"
        self.add_code(code)
        print(self.sem_stack)

    def handle_boolean_exp(self, operand):
        print(self.sem_stack)
        opr2 = self.sem_stack.pop()
        operation = self.sem_stack.pop()
        opr1 = self.sem_stack.pop()
        tmp = self.sym_table.get_temp('BOOL', 1)
        self.add_var(tmp.value)
        self.sem_stack.append(tmp)
        for reg, op in zip(['$t0', '$t1'], [opr1, opr2]):
            if op.type in ['INTEGER', 'REAL_NUMBER']:
                code = f"li {reg}, {op.value}\n"
                self.add_code(code)
            else:
                name, type = self.sym_table.get_name_type(op.value)
                code = f"l{type_asm_map[type]} {reg}, {name}\n"
                self.add_code(code)
        code = f"{operation_map[operation.value]} $t2, $t0, $t1\n"
        self.add_code(code)
        tmp_name, _ = self.sym_table.get_name_type(tmp.value)
        code = f"sw $t2, {tmp_name}\n"
        self.add_code(code)
        print(self.sem_stack)

    def handle_evaluate_be(self, operand):
        pass

    def handle_push_pc(self, operand):
        self.sem_stack.append(self.pc)

    def handle_JZ(self, operand):
        be = self.sem_stack.pop()
        name, _ = self.sym_table.get_name_type(be.value)
        code = f"lb $t0, {name}\n"
        self.add_code(code)
        code = f"beqz $t0, CompleteLater\n"
        print("PC JZ", self.pc)
        self.sem_stack.append(self.pc)
        self.add_code(code)

    def handle_CJZ(self, operand):
        pc = self.sem_stack[-1]
        print("PC: ", pc)
        print(self.code[pc - 1])
        self.code[pc - 1] = f"beqz $t0, PC{self.pc}\n"
        print(self.code[pc - 1])

    def handle_JP(self, operand):
        self.sem_stack.pop()
        be = self.sem_stack.pop()
        name, _ = self.sym_table.get_name_type(be.value)
        code = f"lb $t0, {name}\n"
        self.add_code(code)
        code = f"bnez $t0, CompleteLater\n"
        self.add_code(code)
        self.sem_stack.append(self.pc)

    def handle_CJP(self, operand):
        pc = self.sem_stack[-1]
        print("PC: ", pc)
        print(self.code[pc - 1])
        self.code[pc - 1] = f"bnez $t0, PC{self.pc}\n"
        print(self.code[pc - 1])

    def handle_pop_while(self, operand):
        pc = self.sem_stack.pop()
        print(self.code[pc])
        self.code[pc] = f"beqz $t0, PC{self.pc}\n"
        pc = self.sem_stack.pop()
        code = f"b PC{pc}\n"
        self.add_code(code)

    def handle_push_noass(self, operand):
        self.sem_stack.append('noass')

    def handle_print(self, operand):
        opr = self.sem_stack.pop()
        if opr.type in ['INTEGER', 'REAL_NUMBER']:
            code = f"li $v0, 1\n"
            self.add_code(code)
            code = f"li $t0, {opr.value}\n"
        elif opr.type == 'STRING':
            code = f"li $v0, 4\n"
            self.add_code(code)
            code = f"la $t0, {opr.value}\n"
        else:
            name, type = self.sym_table.get_name_type(opr.value)
            var = self.sym_table.find(opr.value)
            print("FUCKKKK", var)
            if var.type == 'STRING_KEYWORD':
                code = f"li $v0, 4\n"
                self.add_code(code)
            else:
                code = f"li $v0, 1\n"
                self.add_code(code)
            code = f"l{type_asm_map[type]} $a0, {name}\n"
        self.add_code(code)
        code = f"syscall\n"
        self.add_code(code)

    def handle_in_int(self, operand):
        code = f"li $v0, 5\n"
        self.add_code(code)
        code = f"syscall\n"
        self.add_code(code)
        tmp = self.sym_table.get_temp('INT', 1)
        self.add_var(tmp.value)
        tmp_name, _ = self.sym_table.get_name_type(tmp.value)
        code = f"sw $v0, {tmp_name}\n"
        self.add_code(code)
        self.sem_stack.append(tmp)





    def add_code(self, code):
        self.code.append(code)
        self.pc += 1

    def flush(self, path):
        with open(path, 'w') as f:
            self.code = [f"PC{i}:\n       {self.code[i]}" for i in range(len(self.code))]
            print(self.code)
            self.code.append(f"PC{len(self.code)}:\n")
            code_part = ".text\n.globl main\nmain:\n       " + "       ".join(self.code)
            data_part = ".data\n       " + "       ".join(self.data)
            f.write(f"{data_part}\n\n\n{code_part}\n\n\nexit:\n       li $v0, 10\n       syscall")

        print("\n\n\n\n\n\n\n\n")
        # subprocess.run(['spim', '-a', '-f', path,  'd.out'])
