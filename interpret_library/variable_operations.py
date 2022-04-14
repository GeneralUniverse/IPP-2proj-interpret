from interpret_library import interpret_core as ic


def search(name):
    for var in ic.Instruction.variable_list:
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
    ic.Instruction.variable_list.append(var)


def set_value(name, value):
    var = search(name)
    var["value"] = value


def set_type(name, typ):
    var = search(name)
    var["type"] = typ


def get_value(name):
    if name.startswith("GF@"):
        return str(search(name)["value"])
    else:
        return str(name)


def get_type(name):
    typ = search(name)["type"]
    return typ
