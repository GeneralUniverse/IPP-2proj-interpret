import sys
from interpret_library import variable_operations as vo


class Instruction:
    stack = []
    variable_list = []

    def __init__(self, opcode, child, read_input):
        self._opc = opcode.upper()
        self._child = child
        self._list_of_args = []
        self._read_input = read_input

    def get_number_of_args(self):
        return len(self._child.getchildren())

    def _args_to_list(self):
        args = []
        for arg in self._child:
            arg_dic = {
                "type": arg.get("type"),
                "content": arg.text
            }
            args.append(arg_dic)
        return args

    def perform(self):
        arg_num = Instruction.get_number_of_args(self)

        # 1 ARGUMENTS OPERATIONS ##########################

        if arg_num == 1:
            arg1 = Instruction._args_to_list(self)[0]

            if self._opc == "PUSHS":
                Instruction.stack.append(arg1)

            if self._opc == "POPS":
                stack_vals = Instruction.stack.pop()

                vo.declare(arg1["content"], stack_vals["type"])
                vo.set_value(arg1["content"], stack_vals["content"])

            if self._opc == "WRITE":
                sys.stdout.write(vo.get_value(arg1["content"]))

            if self._opc == "DEFVAR":
                vo.declare(arg1["content"], "")

        # 2 ARGUMENTS OPERATIONS ##########################

        if arg_num == 2:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]

            if self._opc == "MOVE":
                var = vo.search(arg1["content"])

                vo.set_value(arg1["content"], vo.get_value(arg2["content"]))

                if var["type"] == "":  # move set up type for defined variables
                    var["type"] = arg2["type"]

            if self._opc == "NOT":
                result = "false"

                if vo.get_value(arg2["content"]) == "false":
                    result = "true"
                if arg2["content"] == "true":
                    result == "false"

                var = var.search(arg1["content"])
                var["type"] = "bool"
                vo.set_value(arg1["content"], result)

            if self._opc == "INT2CHAR":
                val = vo.get_value(arg2["content"])

                try:
                    uni_num = int(val)
                    char = chr(uni_num)
                except:
                    raise exit(58)

                vo.set_type(arg1["content"], "string")
                vo.set_value(arg1["content"], char)

            if self._opc == "READ":
                typ = arg2["content"]
                my_input = self._read_input

                if typ == "string":
                    vo.set_value(arg1["content"], my_input.strip())

                if typ == "int":
                    try:
                        num = int(my_input)
                    except:
                        num = "nil@nil"
                    vo.set_value(arg1["content"], num)

                if typ == "bool":
                    var1 = "false"

                    if my_input.upper() == "TRUE":
                        var1 = "true"

                    vo.set_value(arg1["content"], var1)

            if self._opc == "STRLEN":
                var1 = arg1["content"]

                my_str = vo.get_value(arg2["content"])
                my_str_len = len(my_str)

                vo.set_value(var1, my_str_len)

            if self._opc == "TYPE":
                var1 = arg1["content"]
                var2 = arg2["content"]

                if var2.startswith("GF@"):
                    typ = vo.search(var2)["type"]
                else:
                    typ = arg2["type"]

                vo.set_value(var1, typ)
                # 3 ARGUMENTS OPERATIONS ##########################

        if arg_num == 3:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]
            arg3 = Instruction._args_to_list(self)[2]

            # operations with number
            if self._opc in ("ADD", "SUB", "MUL", "IDIV"):
                if arg2["type"] != "int" or arg3["type"] != "int":
                    exit("pocetni operace s ne cisli")

                num1 = int(vo.get_value(arg2["content"]))
                num2 = int(vo.get_value(arg3["content"]))

                if self._opc == "ADD":
                    result = num1 + num2

                if self._opc == "SUB":
                    result = num1 - num2

                if self._opc == "MUL":
                    result = num1*num2

                if self._opc == "IDIV":
                    if num2 == 0:
                        exit(57)
                    result = num1 / num2

                vo.set_value(arg1["content"], result)

            # comparing instructions
            if self._opc in ("LT", "GT", "EQ"):
                result = "false"
                var1 = vo.get_value(arg2["content"])
                var2 = vo.get_value(arg3["content"])

                if self._opc == "LT":
                    if var1 < var2:
                        result = "true"

                if self._opc == "GT":
                    if var1 > var2:
                        result = "true"

                if self._opc == "EQ":
                    if var1 == var2:
                        result = "true"

                vo.set_type(arg1["content"], "bool")
                vo.set_value(arg1["content"], result)

            # logical instructions # NOT is in 2 argument section
            if self._opc in ("AND", "OR"):
                result = "false"
                var1 = vo.get_value(arg2["content"])
                var2 = vo.get_value(arg3["content"])

                if self._opc == "AND":
                    if var1 == "true" and var2 == "true":
                        result = "true"

                if self._opc == "OR":
                    if var2 == "true" or var1 == "true":
                        result = "true"

                vo.set_type(arg1["content"], "bool")
                vo.set_value(arg1["content"], result)

            # other
            if self._opc == "STRI2INT":
                my_str = vo.get_value(arg2["content"])
                position = int(vo.get_value(arg3["content"]))

                if not(0 < position < len(my_str)):
                    exit(58)

                selected_char = my_str[position]

                vo.set_value(arg1["content"], ord(selected_char))

            if self._opc == "CONCAT":
                var1 = arg1["content"]
                var2 = arg2["type"]
                var3 = arg3["type"]

                if var2 != "string" or var3 != "string":
                    exit("nejaka concat chyba")

                result = arg2["content"] + arg2["content"]

                vo.set_type(var1, "string")
                vo.set_value(var1, result)

            if self._opc == "GETCHAR":
                var1 = arg1["content"]
                my_str = vo.get_value(arg2["content"])
                pos = int(vo.get_value(arg3["content"]))

                if not(0 < pos < len(my_str)):
                    exit(58)

                my_char = my_str[pos]

                vo.set_value(var1, my_char)

            if self._opc == "SETCHAR":
                var1 = arg1["content"]
                pos = int(vo.get_value(arg2["content"]))
                my_char = vo.get_value(arg3["content"])[0]

                temp = vo.get_value(var1)
                temp = temp[:pos] + my_char + temp[pos+1:]

                vo.set_value(var1, temp)
