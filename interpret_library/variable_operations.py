import re

from interpret_library import interpret_core as ic


def search(name):
    currect_list = ic.Instruction.gf_var_list

    if re.match("^TF@", name):
        currect_list = ic.Instruction.tf_var_list
    if re.match("^LF@", name):
        currect_list = ic.Instruction.lf_var_stack[-1]

    for var in currect_list:
        if var["name"] == name:
            return var
    return {
        "name": "",
        "type": "",
        "value": ""
    }


def declare(name, typ):
    var = {
        "name": name,
        "type": typ,
        "value": ""
    }
    if re.match("^TF@", name):
        ic.Instruction.tf_var_list.append(var)
    elif re.match("^GF@", name):
        ic.Instruction.gf_var_list.append(var)
    else:
        exit("nejaka declare chyba")


def set_value(name, value):
    var = search(name)
    var["value"] = value


def set_type(name, typ):
    var = search(name)
    var["type"] = typ


def get_value(name):
    if re.match("^[GF@|LF@|TF@]", name):
        return str(search(name)["value"])
    else:
        return str(name)


def get_type(arg):
    if re.match("^[GF@|LF@|TF@]", arg["content"]):
        return search(arg["content"])["type"]
    else:
        return arg["type"]
