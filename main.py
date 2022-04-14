import sys
import re
from interpret_library import xml_check
from interpret_library import terminal_args_check
from interpret_library.interpret_core import Instruction

if __name__ == '__main__':

    args = terminal_args_check.create_args()

    src = terminal_args_check.get_source(args)
    r_input = terminal_args_check.get_read_input(args)

    root = xml_check.get_root(src)
    root[:] = sorted(root, key=lambda kid: int(kid.get("order")))

    for child in root:
        opc = child.attrib["opcode"]
        r = ""

        if opc == "READ":  # very retarded solution of handling arguments to read function
            if not r_input:
                r = input()
            else:
                r = r_input.readline()

        i = Instruction(opc, child, r)
        i.perform()

    print()
    for var in Instruction.variable_list:
        print(var)


