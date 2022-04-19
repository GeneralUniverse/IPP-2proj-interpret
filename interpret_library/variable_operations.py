import re

from interpret_library import interpret_core as ic


def search(name):
    currect_list = ic.Instruction.gf_var_list

    if re.match("^TF@", name):
        if not ic.Instruction.tf_var_list:
            exit(55)
        currect_list = ic.Instruction.tf_var_list
    if re.match("^LF@", name):
        currect_list = ic.Instruction.lf_var_stack[-1]

    for var in currect_list:
        if var["name"] == name:
            return var
    return {
        exit(54)
    }


def declare(name, typ):
    # can't use search function due to exit 54
    currect_list = ic.Instruction.gf_var_list

    if re.match("^TF@", name):
        if ic.Instruction.tf_var_list is not None:
            currect_list = ic.Instruction.tf_var_list
        else:
            exit(55)

    for var in currect_list:
        if var["name"] == name:
            exit(52)

    var = {
        "name": name,
        "type": typ,
        "value": ""
    }

    if re.match("^TF@", name):
        ic.Instruction.tf_var_list.append(var)
    if re.match("^GF@", name):
        ic.Instruction.gf_var_list.append(var)


def set_value(name, value):
    var = search(name)
    var["value"] = value


def set_type(name, typ):
    var = search(name)
    var["type"] = typ


def get_value(name):
    if name is None:
        return ""

    var1 = ""
    try:
        var1 = str(name)
    except Exception:
        exit(32)

    if re.match("^[GF@|LF@|TF@]", var1):
        return str(search(name)["value"])
    else:
        return str(name)


def get_type(arg):
    var1 = ""
    try:
        var1 = str(arg["content"])
    except Exception:
        exit(32)

    if re.match("^[GF@|LF@|TF@]", var1):
        return search(arg["content"])["type"]
    else:
        return arg["type"]
