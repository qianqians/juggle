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
    OriginalTypeList = [tools.TypeType.Enum, tools.TypeType.String, tools.TypeType.Int8, tools.TypeType.Int16, tools.TypeType.Int32, tools.TypeType.Int64,
                        tools.TypeType.Uint8, tools.TypeType.Uint16, tools.TypeType.Uint32, tools.TypeType.Uint64, 
                        tools.TypeType.Float, tools.TypeType.Double, tools.TypeType.Bool, tools.TypeType.Bin]

    code = "    public:\n"
    code += "        static msgpack11::MsgPack::array " + struct_name + "_to_protcol(" + struct_name + " _struct){\n"
    code += "            msgpack11::MsgPack::array _protocol;\n"
    
    for key, value in elems:
        type_ = tools.check_type(key, dependent_struct, dependent_enum)
        if type_ in OriginalTypeList:
            code += "            _protocol.push_back(_struct." + value + ");\n"
        elif type_ == tools.TypeType.Custom:
            code += "            _protocol.push_back(" + key + "::" + key + "_to_protcol(_struct." + value + "));\n"
        elif type_ == tools.TypeType.Array:
            code += "            msgpack11::MsgPack::array _array_" + value + "(rapidjson::kArrayType);\n"
            code += "            for(var v_ : _struct." + value + "){\n"
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
            if array_type_ in OriginalTypeList:
                code += "                _array_" + value + ".push_back(v_);\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "                _array_" + value + ".push_back(" + array_type + "::" + array_type + "_to_protcol(v_));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "            }\n"
            code += "            _protocol.PushBack(_array_" + value + ", allocator);\n"
    code += "            return _protocol.GetArray();\n"
    code += "        }\n"
    return code

def genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "        static " + struct_name + " protcol_to_" + struct_name + "(rapidjson::Value& _protocol){\n"
    count = 0
    for key, value in elems:
        type_ = tools.check_type(key, dependent_struct, dependent_enum)
        _type_ = tools.convert_type(key, dependent_struct, dependent_enum)
        if type_ == tools.TypeType.Int32:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetInt();\n"
        elif type_ == tools.TypeType.Int64:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetInt64();\n"
        elif type_ == tools.TypeType.Uint32:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetUint();\n"
        elif type_ == tools.TypeType.Uint64:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetUint64();\n"
        elif type_ == tools.TypeType.Float:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetFloat();\n"
        elif type_ == tools.TypeType.Double:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetDouble();\n"
        elif type_ == tools.TypeType.Bool:
            code += "            auto _" + value + " = _protocol[" + str(count) + "].GetBool();\n"
        elif type_ == tools.TypeType.String:
            code += "            std::string _" + value + " = _protocol[" + str(count) + "].GetString();\n"
        elif type_ == tools.TypeType.Custom:
            code += "            auto _" + value + " = " + key + "::protcol_to_" + key + "(_protocol[" + str(count) + "]);\n"
        elif type_ == tools.TypeType.Array:
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
            _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
            code += "            std::vector<" + _array_type + "> _" + value + ";\n"
            _v_uuid = str(uuid.uuid1())
            _v_uuid = '_'.join(_v_uuid.split('-'))
            code += "            for(auto it_" + _v_uuid + " = _protocol[" + str(count) + "].Begin(); it" + _v_uuid + " != _protocol[" + str(count) + "].End(); ++it" + _v_uuid + "){\n"
            if array_type_ == tools.TypeType.Int32:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetInt());\n"
            elif array_type_ == tools.TypeType.Int64:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetInt64());\n"
            elif array_type_ == tools.TypeType.Uint32:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetUint());\n"
            elif array_type_ == tools.TypeType.Uint64:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetUint64());\n"
            elif array_type_ == tools.TypeType.Float:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetFloat());\n"
            elif array_type_ == tools.TypeType.Double:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetDouble());\n"
            elif array_type_ == tools.TypeType.Bool:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetBool());\n"
            elif array_type_ == tools.TypeType.String:
                code += "        _" + value + ".push_back(it_" + _v_uuid + "->GetString());\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "        _" + value + ".push_back(" + array_type + "::protcol_to_" + array_type + "(it_" + _v_uuid + "));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "            }\n"
        count = count + 1
    code += "            " + struct_name + " _struct("
    count = 0
    for key, value in elems:
        code += "_" + value
        count = count + 1
        if count < len(elems):
            code += ", "
    code += ");\n"
    code += "            return _struct;\n"
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
