import sys


def _search_var(name):
    for var in Instruction.variable_list:
        if var["name"] == name:
            return var
    return {
        "name": "",
        "type": "",
        "value": ""
    }


def _declare_variable(name, typ):
    var = {
        "name": name,
        "type": typ,
        "value": ""
    }

    Instruction.variable_list.append(var)


def _set_variable_value(name, value):
    var = _search_var(name)
    var["value"] = value


def _set_variable_type(name, typ):
    var = _search_var(name)
    var["type"] = typ


def _get_value(name):
    if name.startswith("GF@"):
        return _search_var(name)["value"]
    else:
        return name


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

                _declare_variable(arg1["content"], stack_vals["type"])
                _set_variable_value(arg1["content"], stack_vals["content"])

            if self._opc == "WRITE":
                var = _search_var(arg1["content"])

                sys.stdout.write(str(var["value"])+"\n")

            if self._opc == "DEFVAR":
                _declare_variable(arg1["content"], "")

        # 2 ARGUMENTS OPERATIONS ##########################

        if arg_num == 2:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]

            if self._opc == "MOVE":
                var = _search_var(arg1["content"])

                _set_variable_value(arg1["content"], _get_value(arg2["content"]))

                if var["type"] == "":  # move set up type for defined variables
                    var["type"] = arg2["type"]

            if self._opc == "NOT":
                result = "false"

                if _get_value(arg2["content"]) == "false":
                    result = "true"
                if arg2["content"] == "true":
                    result == "false"

                var = _search_var(arg1["content"])
                var["type"] = "bool"
                _set_variable_value(arg1["content"], result)

            if self._opc == "INT2CHAR":
                val = _get_value(arg2["content"])

                try:
                    uni_num = int(val)
                    char = chr(uni_num)
                except:
                    raise exit(58)

                _set_variable_type(arg1["content"], "string")
                _set_variable_value(arg1["content"], char)

            if self._opc == "READ":
                typ = arg2["content"]
                my_input = self._read_input

                if typ == "string":
                    _set_variable_value(arg1["content"], my_input)

                if typ == "int":
                    num = 0

                    try:
                        num = int(my_input)
                    except:
                        num = "nil@nil"

                    _set_variable_value(arg1["content", num])

        # 3 ARGUMENTS OPERATIONS ##########################

        if arg_num == 3:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]
            arg3 = Instruction._args_to_list(self)[2]

            # operations with number
            if self._opc in ("ADD", "SUB", "MUL", "IDIV"):
                if arg2["type"] != "int" or arg3["type"] != "int":
                    exit("pocetni operace s ne cisli")

                num1 = int(_get_value(arg2["content"]))
                num2 = int(_get_value(arg3["content"]))

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

                _set_variable_value(arg1["content"], result)

            # comparing instructions
            if self._opc in ("LT", "GT", "EQ"):
                result = "false"
                var1 = _get_value(arg2["content"])
                var2 = _get_value(arg3["content"])

                if self._opc == "LT":
                    if var1 < var2:
                        result = "true"

                if self._opc == "GT":
                    if var1 > var2:
                        result = "true"

                if self._opc == "EQ":
                    if var1 == var2:
                        result = "true"

                _set_variable_type(arg1["content"], "bool")
                _set_variable_value(arg1["content"], result)

            # logical instructions
            if self._opc in ("AND", "OR"):  # NOT is in 2 argument section
                result = "false"
                var1 = _get_value(arg2["content"])
                var2 = _get_value(arg3["content"])

                if self._opc == "AND":
                    if var1 == "true" and var2 == "true":
                        result = "true"

                if self._opc == "OR":
                    if var2 == "true" or var1 == "true":
                        result = "true"

                _set_variable_type(arg1["content"], "bool")
                _set_variable_value(arg1["content"], result)

            # other
            if self._opc == "STRI2INT":
                my_str = _get_value(arg2["content"])
                position = int(_get_value(arg3["content"]))

                if not(0 < position < len(my_str)):
                    exit(58)

                selected_char = my_str[position]

                _set_variable_value(arg1["content"], ord(selected_char))

