import sys
import re
from interpret_library import xml_check as xml
from interpret_library import terminal_args_check

if __name__ == '__main__':

    args = terminal_args_check.createArgs()

    src = terminal_args_check.getSource(args)
    rInput = terminal_args_check.getReadInput(args)

    root = xml.getRoot(src)

    print(root.tag)
