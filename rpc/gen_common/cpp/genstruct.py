#coding:utf-8
# 2019-12-27
# build by qianqians
# genstruct

import tools
import uuid

def genmainstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "    class " + struct_name + " {\n"
    code += "    public:\n"
    names = []
    for key, value in elems:
        if value in names:
            raise Exception("repeat struct elem:%s in struct:%s" % (key, struct_name))
        names.append(value)
        code += "        " + tools.convert_type(key, dependent_struct, dependent_enum) + " " + value + ";\n"
    code += "\n    public:\n"
    code += "        " + struct_name + "("
    count = 0
    for key, value in elems:
        code += tools.convert_type(key, dependent_struct, dependent_enum) + " " +"_" + value 
        count = count + 1
        if count < len(elems):
            code += ", "
    code += "){\n"
    for key, value in elems:
        code += "            " + value + " = _" + value + ";\n"
    code += "        }\n\n" 
    code += "        " + struct_name + "() = default;\n\n"
    code += "        " + struct_name + "(" + struct_name + "& value) = default;\n\n"
    return code

def genstructprotocol(struct_name, elems, dependent_struct, dependent_enum):
    code = "    public:\n"
    code += "        static msgpack11::MsgPack::array " + struct_name + "_to_protcol(" + struct_name + " _struct){\n"
    code += "            msgpack11::MsgPack::array _protocol;\n"
    
    for key, value in elems:
        type_ = tools.check_type(key, dependent_struct, dependent_enum)
        if type_ in tools.OriginalTypeList:
            code += "            _protocol.push_back(_struct." + value + ");\n"
        elif type_ == tools.TypeType.Custom:
            code += "            _protocol.push_back(" + key + "::" + key + "_to_protcol(_struct." + value + "));\n"
        elif type_ == tools.TypeType.Array:
            code += "            msgpack11::MsgPack::array _array_" + value + ";\n"
            code += "            for(var v_ : _struct." + value + "){\n"
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
            if array_type_ in tools.OriginalTypeList:
                code += "                _array_" + value + ".push_back(v_);\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "                _array_" + value + ".push_back(" + array_type + "::" + array_type + "_to_protcol(v_));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "            }\n"
            code += "            _protocol.push_back(_array_" + value + ");\n"
    code += "            return _protocol;\n"
    code += "        }\n"
    return code

def genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "        static " + struct_name + " protcol_to_" + struct_name + "(msgpack11::MsgPack::array& _protocol){\n"
    count = 0
    for key, value in elems:
        type_ = tools.check_type(key, dependent_struct, dependent_enum)
        _type_ = tools.convert_type(key, dependent_struct, dependent_enum)
        if type_ == tools.TypeType.Int8:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].int8_value();\n"
        elif type_ == tools.TypeType.Int16:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].int16_value();\n"
        elif type_ == tools.TypeType.Int32:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].int32_value();\n"
        elif type_ == tools.TypeType.Int64:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].int64_value();\n"
        elif type_ == tools.TypeType.Uint8:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].uint8_value();\n"
        elif type_ == tools.TypeType.Uint16:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].uint16_value();\n"
        elif type_ == tools.TypeType.Uint32:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].uint32_value();\n"
        elif type_ == tools.TypeType.Uint64:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].uint64_value();\n"
        elif type_ == tools.TypeType.Float:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].float32_value();\n"
        elif type_ == tools.TypeType.Double:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].float64_value();\n"
        elif type_ == tools.TypeType.Bool:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].bool_value();\n"
        elif type_ == tools.TypeType.String:
            code += "            std::string _" + value + " = _protocol[" + str(count) + "].string_value();\n"
        elif type_ == tools.TypeType.Bin:
            code += "            std::string _" + value + " = _protocol[" + str(count) + "].binary_items();\n"
        elif type_ == tools.TypeType.Custom:
            code += "            auto _" + value + " = " + key + "::protcol_to_" + key + "(_protocol[" + str(count) + "]);\n"
        elif type_ == tools.TypeType.Array:
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
            _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
            code += "            std::vector<" + _array_type + "> _" + value + ";\n"
            code += "            auto _protocol_array = _protocol[" + str(count) + "].array_items();n"
            code += "            for(auto it_ : _protocol_array){\n"
            if array_type_ == tools.TypeType.Int8:
                code += "        _" + value + ".push_back(it_.int8_value());\n"
            elif array_type_ == tools.TypeType.Int16:
                code += "        _" + value + ".push_back(it_.int16_value());\n"
            elif array_type_ == tools.TypeType.Int32:
                code += "        _" + value + ".push_back(it_.int32_value());\n"
            elif array_type_ == tools.TypeType.Int64:
                code += "        _" + value + ".push_back(it_.int64_value());\n"
            elif array_type_ == tools.TypeType.Uint8:
                code += "        _" + value + ".push_back(it_.uint8_value());\n"
            elif array_type_ == tools.TypeType.Uint16:
                code += "        _" + value + ".push_back(it_.uint16_value());\n"
            elif array_type_ == tools.TypeType.Uint32:
                code += "        _" + value + ".push_back(it_.uint32_value());\n"
            elif array_type_ == tools.TypeType.Uint64:
                code += "        _" + value + ".push_back(it_.uint64_value());\n"
            elif array_type_ == tools.TypeType.Float:
                code += "        _" + value + ".push_back(it_.float32_value());\n"
            elif array_type_ == tools.TypeType.Double:
                code += "        _" + value + ".push_back(it_.float64_value());\n"
            elif array_type_ == tools.TypeType.Bool:
                code += "        _" + value + ".push_back(it_.bool_value());\n"
            elif array_type_ == tools.TypeType.String:
                code += "        _" + value + ".push_back(it_.string_value());\n"
            elif array_type_ == tools.TypeType.Bin:
                code += "        _" + value + ".push_back(it_.binary_items());\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "        _" + value + ".push_back(" + array_type + "::protcol_to_" + array_type + "(it_" + _v_uuid + "));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "            }\n"
        count = count + 1
    _struct_uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, struct_name)).split('-'))
    code += "            " + struct_name + " _struct" + _struct_uuid + "("
    count = 0
    for key, value in elems:
        code += "_" + value
        count = count + 1
        if count < len(elems):
            code += ", "
    code += ");\n"
    code += "            return _struct" + _struct_uuid + ";\n"
    code += "        }\n"
    return code

def genstruct(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    struct = pretreatment.struct
    
    code = "/*this struct code is codegen by abelkhan codegen for cpp*/\n"
    for struct_name, elems in struct.items():
        code += genmainstruct(struct_name, elems, dependent_struct, dependent_enum)
        code += genstructprotocol(struct_name, elems, dependent_struct, dependent_enum)
        code += genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum)
        code += "    };\n\n"

    return code