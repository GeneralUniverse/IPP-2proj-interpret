import re
import sys
from interpret_library import variable_operations as vo


class Instruction:
    var_stack = []
    gf_var_list = []
    tf_var_list = None
    lf_var_stack = []
    label_list = []

    def __init__(self, child, read_input, numb):
        self._opc = child.attrib["opcode"].upper()
        self._child = child
        self._read_input = read_input
        self._numb = numb

    def _get_number_of_args(self):
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

    def execute(self):
        arg_num = Instruction._get_number_of_args(self)

        ###################################################
        # 0 ARGUMENTS INSTRUCTIONS ##########################
        ###################################################

        if arg_num == 0:
            if self._opc == "CREATEFRAME":
                Instruction.tf_var_list = []

            if self._opc == "PUSHFRAME":
                if not Instruction.tf_var_list:
                    exit(55)

                for tf_var in Instruction.tf_var_list:
                    tf_var["name"] = re.sub("^TF@", "LF@", tf_var["name"])

                Instruction.lf_var_stack.append(Instruction.tf_var_list)

            if self._opc == "POPFRAME":
                if not Instruction.lf_var_stack:
                    exit(55)

                Instruction.tf_var_list = Instruction.lf_var_stack.pop()

                for lf_var in Instruction.tf_var_list:
                    lf_var["name"] = re.sub("^LF@", "TF@", lf_var["name"])

        ###################################################
        # 1 ARGUMENTS INSTRUCTIONS ##########################
        ###################################################

        if arg_num == 1:
            arg1 = Instruction._args_to_list(self)[0]

            if self._opc == "PUSHS":
                Instruction.var_stack.append(arg1)

            if self._opc == "POPS":
                var_stack_vals = Instruction.var_stack.pop()

                vo.declare(arg1["content"], var_stack_vals["type"])
                vo.set_value(arg1["content"], var_stack_vals["content"])

            if self._opc == "WRITE":
                sys.stdout.write(vo.get_value(arg1["content"]))

            if self._opc == "DEFVAR":
                vo.declare(arg1["content"], "")

            if self._opc == "JUMP":
                var1 = arg1["content"]

                num = _get_label_number(var1, self._numb)
                self._numb = num

            if self._opc == "EXIT":
                var1 = vo.get_value(arg1["content"])

                if not(re.match("[0-49]", var1)):
                    exit(57)
                sys.stdout.write(var1)

            if self._opc == "DPRINT":
                err_message = vo.get_value(arg1["content"])
                sys.stderr.write(err_message)

            # TODO - BREAK

        ###################################################
        # 2 ARGUMENTS INSTRUCTIONS ##########################
        ###################################################

        if arg_num == 2:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]

            if self._opc == "MOVE":
                vo.set_value(arg1["content"], vo.get_value(arg2["content"]))

                # TODO - type condition
                vo.set_type(arg1["content"], arg2["type"])

            if self._opc == "NOT":
                result = "false"

                if vo.get_value(arg2["content"]) == "false":
                    result = "true"
                elif arg2["content"] == "true":
                    result = "false"
                else:
                    exit("SOMETHING")

                # TODO - make function for it
                # var1 = var.search(arg1["content"])
                # var1["type"] = "bool"
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

        ###################################################
        # 3 ARGUMENTS INSTRUCTIONS ##########################
        ###################################################

        if arg_num == 3:
            arg1 = Instruction._args_to_list(self)[0]
            arg2 = Instruction._args_to_list(self)[1]
            arg3 = Instruction._args_to_list(self)[2]

            # INSTRUCTIONS with numbers
            if self._opc in ("ADD", "SUB", "MUL", "IDIV"):
                if vo.get_type(arg2) != "int" or vo.get_type(arg3) != "int":
                    exit(53)

                num1 = int(vo.get_value(arg2["content"]))
                num2 = int(vo.get_value(arg3["content"]))
                result = 0

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
                vo.set_type(arg1["content"], "int")

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

            if self._opc == "JUMPIFEQ":
                var1 = arg1["content"]
                var2 = vo.get_value(arg2["content"])
                var3 = vo.get_value(arg3["content"])
                num = self._numb

                if var2 == var3:
                    num = _get_label_number(var1, self._numb)

                self._numb = num

            if self._opc == "JUMPIFNEQ":
                var1 = arg1["content"]
                var2 = vo.get_value(arg2["content"])
                var3 = vo.get_value(arg3["content"])
                num = self._numb

                if var2 != var3:
                    num = _get_label_number(var1, self._numb)

                self._numb = num

    def get_position_of_next_instruction(self):
        return self._numb

    def add_label_to_list(self):
        if self._opc == "LABEL":
            arg1 = Instruction._args_to_list(self)[0]

            label_dic = {
                "name": arg1["content"],
                "number": self._numb
            }

            for label in Instruction.label_list:
                if label["name"] == arg1["content"]:
                    exit(52)

            Instruction.label_list.append(label_dic)


def get_read_input(r_input, opc):
    if opc == "READ":
        if not r_input:
            r = input()
        else:
            r = r_input.readline()
        return r


def _get_label_number(name, current_line_number):
    for i in Instruction.label_list:
        if i["name"] == name:
            return int(i["number"])
    return current_line_number
