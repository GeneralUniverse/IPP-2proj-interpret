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


def _init_variable(name, value):
    for var in Instruction.variable_list:
        if var["name"] == name:
            var["value"] = value


class Instruction:
    stack = []
    variable_list = []

    def __init__(self, opcode, child):
        self._opc = opcode.upper()
        self._child = child
        self._list_of_args = []

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

        if arg_num == 1:
            arg1 = Instruction._args_to_list(self)[0]

            if self._opc == "PUSHS":
                Instruction.stack.append(arg1)

            if self._opc == "POPS":
                stack_vals = Instruction.stack.pop()

                _declare_variable(arg1["content"], stack_vals["type"])
                _init_variable(arg1["content"], stack_vals["content"])

            if self._opc == "WRITE":
                var = _search_var(arg1["content"])

                print(var["value"])

            if self._opc == "DEFVAR":
                _declare_variable(arg1["content"], "")

        if arg_num == 2:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]

            if self._opc == "MOVE":
                var = _search_var(arg1["content"])

                _init_variable(arg1["content"], arg2["content"])

                if var["type"] == "":
                    var["type"] = arg2["type"]

        if arg_num == 3:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]
            arg3 = Instruction._args_to_list(self)[2]

            # operations with number
            if self._opc in ("ADD", "SUB", "MUL", "IDIV"):
                if arg2["type"] != "int" or arg3["type"] != "int":
                    exit("pocetni operace s ne cisli")

                num1 = int(arg2["content"])
                num2 = int(arg3["content"])

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

                _init_variable(arg1["content"], result)

            # comparing instructions
            if self._opc in ("LT", "GT", "EQ"):
                result = "false"

                if self._opc == "LT":
                    if arg2["content"] < arg3["content"]:
                        result = "true"

                if self._opc == "GT":
                    if arg2["content"] > arg3["content"]:
                        result = "true"

                if self._opc == "EQ":
                    if arg2["content"] == arg3["content"]:
                        result = "true"

                _init_variable(arg1["content"], result)

            # logical instructions
            if self._opc in ("AND", "OR"):  # NOT is in 2 argument section
                result = "false"

                if self._opc == "AND":
                    if arg2["content"] == "true" and arg3["content"] == "true":
                        result = "true"

                if self._opc == "OR":
                    if (arg3["content"]) == "true" or bool(arg3["content"] == "true"):
                        result = "true"

                _init_variable(arg1["content"], result)


