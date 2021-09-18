#coding:utf-8
# 2019-12-26
# build by qianqians
# tools

class TypeType():
    Original = 0
    Custom = 1
    Array = 2

def check_in_dependent(typestr, dependent):
    for _type, _import in dependent:
        if _type == typestr:
            return True
    return False

def get_import(typestr, dependent):
    for _type, _import in dependent:
        if _type == typestr:
            return _import
    return ""

def check_type(typestr, dependent_struct, dependent_enum):
    if typestr == 'int32':
        return TypeType.Original
    elif typestr == 'int64':
        return TypeType.Original
    elif typestr == 'uint32':
        return TypeType.Original
    elif typestr == 'uint64':
        return TypeType.Original
    elif typestr == 'string':
        return TypeType.Original
    elif typestr == 'float':
        return TypeType.Original
    elif typestr == 'double':
        return TypeType.Original
    elif typestr == 'bool':
        return TypeType.Original
    elif check_in_dependent(typestr, dependent_struct):
	    return TypeType.Custom
    elif check_in_dependent(typestr, dependent_enum):
    	return TypeType.Original
    elif typestr[len(typestr)-2] == '[' and typestr[len(typestr)-1] == ']':
        return TypeType.Array

    raise Exception("non exist type:%s" % typestr)

def convert_type(typestr, dependent_struct, dependent_enum):
    if typestr == 'int32':
        return 'number'
    elif typestr == 'int64':
        return 'number'
    elif typestr == 'uint32':
        return 'number'
    elif typestr == 'uint64':
        return 'number'
    elif typestr == 'string':
        return 'string'
    elif typestr == 'float':
        return 'number'
    elif typestr == 'double':
        return 'number'
    elif typestr == 'bool':
        return 'boolean'
    elif check_in_dependent(typestr, dependent_struct):
        _import = get_import(typestr, dependent_struct)
        if _import == "":
            return typestr
        else:
            return _import + "." + typestr
    elif check_in_dependent(typestr, dependent_enum):
        _import = get_import(typestr, dependent_enum)
    	if _import == "":
            return typestr
        else:
            return _import + "." + typestr
    elif typestr[len(typestr)-2] == '[' and typestr[len(typestr)-1] == ']':
        array_type = typestr[:-2]
        array_type = convert_type(array_type, dependent_struct, dependent_enum)
        return array_type+'[]'

    raise Exception("non exist type:%s" % typestr)
    
