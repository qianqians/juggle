#coding:utf-8
# 2019-12-27
# build by qianqians
# genstruct

import tools
import uuid

def genmainstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "    public class " + struct_name + "\n    {\n"
    names = []
    for key, value in elems:
        if value in names:
            raise Exception("repeat struct elem:%s in struct:%s" % (key, struct_name))
        names.append(value)
        code += "        public " + tools.convert_type(key, dependent_struct, dependent_enum) + " " + value + ";\n"
    code += "\n        public " + struct_name + "("
    count = 0
    for key, value in elems:
        code += tools.convert_type(key, dependent_struct, dependent_enum) + " " +  "_" + value
        count = count + 1
        if count < len(elems):
            code += ", "
    code += "){\n"
    for key, value in elems:
        code += "            " + value + " = _" + value + ";\n"
    code += "        }\n" 
    return code

def genstructprotocol(struct_name, elems, dependent_struct, dependent_enum):
    code = "        public static JArray " + struct_name + "_to_protcol(" + struct_name + " _struct){\n"
    code += "            var _protocol = new JArray();\n"
    for key, value in elems:
        type_ = tools.check_type(key, dependent_struct, dependent_enum)
        if type_ == tools.TypeType.Original:
            code += "            _protocol.Add(_struct." + value + ");\n"
        elif type_ == tools.TypeType.Custom:
            code += "            _protocol.Add(" + key + "." + key + "_to_protcol(_struct." + value + "));\n"
        elif type_ == tools.TypeType.Array:
            _array_uuid = str(uuid.uuid1())
            _array_uuid = '_'.join(_array_uuid.split('-'))
            code += "            var _array_" + _array_uuid + " = new JArray();"
            _v_uuid = str(uuid.uuid1())
            _v_uuid = '_'.join(_v_uuid.split('-'))
            code += "            foreach(var v_" + _v_uuid + " in _struct." + value + "){\n"
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
            if array_type_ == tools.TypeType.Original:
                code += "                _array_" + _array_uuid + ".Add(v_" + _v_uuid + ");\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "                _array_" + _array_uuid + ".Add(" + array_type + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "            }\n"
            code += "            _protocol.Add(_array_" + _array_uuid + ");\n"
    code += "            return _protocol;\n"
    code += "        }\n"
    return code

def genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "        public static " + struct_name + " protcol_to_" + struct_name + "(JArray _protocol){\n"
    count = 0
    for key, value in elems:
        type_ = tools.check_type(key, dependent_struct, dependent_enum)
        _type_ = tools.convert_type(key, dependent_struct, dependent_enum)
        if type_ == tools.TypeType.Original:
            code += "            var _" + value + " = (" + _type_ + ")_protocol[" + str(count) + "];\n"
        elif type_ == tools.TypeType.Custom:
            code += "            var _" + value + " = " + key + ".protcol_to_" + key + "(_protocol[" + str(count) + "]);\n"
        elif type_ == tools.TypeType.Array:
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
            _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
            code += "            var _" + value + " = new List<" + _array_type + ">();\n"
            _v_uuid = str(uuid.uuid1())
            _v_uuid = '_'.join(_v_uuid.split('-'))
            code += "            foreach(var v_" + _v_uuid + " in _protocol[" + str(count) + "]){\n"
            if array_type_ == tools.TypeType.Original:
                code += "            _" + value + ".Add((" + _array_type + ")v_" + _v_uuid + ");\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "            _" + value + ".Add(" + array_type + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "            }\n"
        count = count + 1
    code += "            var _struct = new " + struct_name + "("
    count = 0
    for key, value in elems:
        code += "_" + value
        count = count + 1
        if count < len(elems):
            code += ","
    code += ");\n"
    code += "            return _struct;\n"
    code += "        }\n"
    return code

def genstruct(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    struct = pretreatment.struct
    
    code = "/*this struct code is codegen by abelkhan codegen for c#*/\n"
    for struct_name, elems in struct.items():
        code += genmainstruct(struct_name, elems, dependent_struct, dependent_enum)
        code += genstructprotocol(struct_name, elems, dependent_struct, dependent_enum)
        code += genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum)
        code += "    }\n\n"

    return code
