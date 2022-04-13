
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
                "value": arg.text
            }
            args.append(arg_dic)
            return args

    def perform(self):
        if self._opc == "PUSHS":
            args = Instruction._args_to_list(self)
            Instruction.stack.append(args[0]["value"])

        if self.opc == "POP":



class IArgument:
    def __init__(self, typ, value):
        self._typ = typ
        self._value = value

