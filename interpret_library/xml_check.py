import xml.etree.ElementTree as etree
import re


def _check_program_element(tree):
    root = tree.getroot()

    if root.tag != 'program':
        exit(32)
    if  "language" not in root.attrib.keys():
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
    for child in tree.getroot():
        for child_child in child:
            if not (re.match("arg[123]", child_child.tag)):
                exit(32)
            if "type" not in child_child.attrib.keys():
                exit(32)


def get_root(src):
    try:
        tree = etree.parse(src)
    except:
        raise exit(31)

    _check_program_element(tree)
    _check_instructions(tree)
    _check_args(tree)

    return tree.getroot()
