import xml.etree.ElementTree as etree
from operator import attrgetter
from interpret_library.interpret_core import Instruction
import re


def _check_program_element(tree):
    root = tree.getroot()

    if root.tag != 'program':
        exit(32)
    if "language" not in root.attrib.keys():
        exit(32)
    if "IPPcode22" not in root.attrib.values():
        exit(32)


def _check_instructions(tree):
    for child in tree.getroot():
        if child.tag != "instruction":
            exit(32)
        if "order" not in child.attrib.keys() or "opcode" not in child.attrib.keys():
            exit(32)


def _check_args(tree):
    random_arg_list = []  # i just wanna check if there is arg1 if there is arg2 with this very dumb solution
    for child in tree.getroot():
        child = _sort_args(child)

        for child_child in child:

            if not (re.match("arg[123]", child_child.tag)):
                exit(32)
            if "type" not in child_child.attrib.keys():
                exit(32)

            random_arg_list.append(child_child.tag)

        if "arg2" in random_arg_list and not "arg1" in random_arg_list:
            exit(32)
        if "arg3" in random_arg_list and not "arg1" in random_arg_list and not "arg2" in random_arg_list:
            exit(32)

        if child.tag.upper() != "INSTRUCTION":
            exit(32)


def _check_order(tree):
    for child in tree.getroot():
        i = 0
        for child2 in tree.getroot():
            if child.attrib["order"] == child2.attrib["order"]:
                i += 1
        if i > 1:  # if it matches more than once (with i()
            exit(32)

        if not re.match("[1-9][0-9]*", child.attrib["order"]):
            exit(32)


def _sort_args(node):
    node[:] = sorted(node, key=attrgetter("tag"))
    return node


def get_root(src):
    try:
        tree = etree.parse(src)
    except:
        raise exit(31)

    _check_program_element(tree)
    _check_instructions(tree)
    _check_args(tree)
    _check_order(tree)

    return tree.getroot()


def opcode_and_no_args_check(self, opc):
    # check validity of opcode and number of argument in instruction
    zero_arg_instr = ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN"]
    one_arg_instr = ["PUSHS", "POPS", "WRITE", "DEFVAR", "JUMP", "EXIT", "DPRINT", "BREAK", "CALL", "LABEL"]
    two_arg_instr = ["MOVE", "NOT", "INT2CHAR", "READ", "STRLEN", "TYPE"]
    three_arg_instr = ["ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "STRI2INT",
                       "CONCAT", "GETCHAR", "SETCHAR", "JUMPIFEQ", "JUMPIFNEQ"]

    if opc not in zero_arg_instr and opc not in one_arg_instr and opc not in two_arg_instr and opc not in three_arg_instr:
        exit(32)
    if Instruction.get_number_of_args(self) == 0 and opc not in zero_arg_instr:
        exit(32)
    if Instruction.get_number_of_args(self) == 1 and opc not in one_arg_instr:
        exit(32)
    if Instruction.get_number_of_args(self) == 2 and opc not in two_arg_instr:
        exit(32)
    if Instruction.get_number_of_args(self) == 3 and opc not in three_arg_instr:
        exit(32)
