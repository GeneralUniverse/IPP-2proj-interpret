import xml.etree.ElementTree as etree
import re


def _checkProgramTag(tree):
    root = tree.getroot()

    if root.tag != 'program':
        exit(32)
    if "name" not in root.attrib.keys() or "language" not in root.attrib.keys():
        exit(32)
    if "IPPcode22" not in root.attrib.values():
        exit(32)


def _checkInstructions(tree):
    for child in tree.getroot():
        if child.tag != "instruction":
            exit(32)
        if "order" not in child.attrib.keys() or "opcode" not in child.attrib.keys():
            exit(32)


def _checkArgs(tree):
    for child in tree.getroot():
        for childchild in child:
            if not (re.match("arg[123]", childchild.tag)):
                exit(32)
            if not "type" in childchild.attrib.keys():
                exit(32)


def getRoot(src):
    try:
        tree = etree.parse(src)
    except:
        raise exit(31)

    _checkProgramTag(tree)
    _checkInstructions(tree)
    _checkArgs(tree)

    return tree.getroot()
