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
        if self._opc == "PUSHS":
            arg1 = Instruction._args_to_list(self)[0]
            Instruction.stack.append(arg1)

        if self._opc == "POPS":
            arg1 = Instruction._args_to_list(self)[0]
            stack_vals = Instruction.stack.pop()

            _declare_variable(arg1["content"], stack_vals["type"])
            _init_variable(arg1["content"], stack_vals["content"])

        if self._opc == "WRITE":
            arg1 = Instruction._args_to_list(self)[0]
            var = _search_var(arg1["content"])

            print(var["value"])

        if self._opc == "MOVE":
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]

            var = _search_var(arg1["content"])

            _init_variable(arg1["content"], arg2["content"])

            if var["type"] == "":
                var["type"] = arg2["type"]

        if self._opc == "DEFVAR":
            arg1 = Instruction._args_to_list(self)[0]

            _declare_variable(arg1["content"], "")


