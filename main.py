import sys
import re
from interpret_library import xml_check
from interpret_library import terminal_args_check
from interpret_library.interpret_core import Instruction
import interpret_library.interpret_core as ic

if __name__ == '__main__':

    args = terminal_args_check.create_args()

    src = terminal_args_check.get_source(args)
    r_input = terminal_args_check.get_read_input(args)

    root = xml_check.get_root(src)
    root[:] = sorted(root, key=lambda kid: int(kid.get("order")))

    instruction_list = []
    label_list = []

    i = 0
    for child in root:
        opc = child.attrib["opcode"].upper()
        ri = ic.get_read_input(r_input, opc)

        instruction_list.append(Instruction(child, ri, i))
        i += 1

    i = 0
    while i < len(root):
        instruction_list[i].execute()
        i = instruction_list[i].get_position_of_next_instruction()
        i = i + 1

    print()
    for var in Instruction.variable_list:
        print(var)


