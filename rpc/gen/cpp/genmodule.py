#coding:utf-8
# 2020-1-21
# build by qianqians
# genmodule

import uuid
import tools

def gen_module_module(module_name, funcs, dependent_struct, dependent_enum):
    code_constructor = "    class " + module_name + "_module : Imodule, public std::enable_shared_from_this<" + module_name + "_module>{\n"
    code_constructor += "    public:\n"
    code_constructor += "        " + module_name + "_module() : Imodule(\"" + module_name + "\")\n"
    code_constructor += "        {\n"
    code_constructor += "        }\n\n"
    code_constructor += "        void Init(std::shared_ptr<modulemng> _modules){\n"
    code_constructor += "            _modules->reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));\n\n"
        
    code_constructor_cb = ""
    rsp_code = ""
    code_func = ""
    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code_constructor += "            reg_method(\"" + func_name + "\", std::bind(&" + module_name + "_module::" + func_name + ", this, std::placeholders::_1));\n"
                
            code_func += "        signals<void("
            count = 0
            for _type, _name in i[2]:
                code_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count += 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ")> sig_" + func_name + ";\n"

            code_func += "        void " + func_name + "(rapidjson::Value& inArray){\n"
            count = 0 
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Int32:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetInt();\n"
                elif type_ == tools.TypeType.Int64:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetInt64();\n"
                elif type_ == tools.TypeType.Uint32:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetUint();\n"
                elif type_ == tools.TypeType.Uint64:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetUint64();\n"
                elif type_ == tools.TypeType.Float:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetFloat();\n"
                elif type_ == tools.TypeType.Double:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetDouble();\n"
                elif type_ == tools.TypeType.Bool:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetBool();\n"
                elif type_ == tools.TypeType.String:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetString();\n"
                elif type_ == tools.TypeType.Custom:
                    code_func += "            auto _" + _name + " = " + _type + "::protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    code_func += "            std::vector<" + _array_type + "> _" + _name + ";\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code_func += "            for(auto it_" + _v_uuid + " = inArray[" + str(count) + "].Begin(); it_" + _v_uuid + " != inArray[" + str(count) + "].End(); ++it_" + _v_uuid + "){\n"
                    if array_type_ == tools.TypeType.Int32:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetInt());\n"
                    elif array_type_ == tools.TypeType.Int64:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetInt64());\n"
                    elif array_type_ == tools.TypeType.Uint32:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetUint());\n"
                    elif array_type_ == tools.TypeType.Uint64:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetUint64());\n"
                    elif array_type_ == tools.TypeType.Float:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetFloat());\n"
                    elif array_type_ == tools.TypeType.Double:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetDouble());\n"
                    elif array_type_ == tools.TypeType.Bool:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetBool());\n"
                    elif array_type_ == tools.TypeType.String:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetString());\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code_func += "                _" + _name + ".push_back(" + array_type + "::protcol_to_" + array_type + "(*it_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code_func += "            }\n"                                                     
                count += 1

            code_func += "            sig_" + func_name + ".emit("
            count = 0
            for _type, _name in i[2]:
                code_func += "_" + _name
                count = count + 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ");\n"
            code_func += "        }\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            code_constructor += "            reg_method(\"" + func_name + "\", std::bind(&" + module_name + "_module::" + func_name + ", this, std::placeholders::_1));\n"
            
            code_func += "        signals<void("
            count = 0
            for _type, _name in i[2]:
                code_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count += 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ")> sig_" + func_name + ";\n"
            
            code_func += "        void " + func_name + "(rapidjson::Value& inArray){\n"
            code_func += "            auto _cb_uuid = inArray[0].GetString();\n"
            count = 1 
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Int32:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetInt();\n"
                elif type_ == tools.TypeType.Int64:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetInt64();\n"
                elif type_ == tools.TypeType.Uint32:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetUint();\n"
                elif type_ == tools.TypeType.Uint64:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetUint64();\n"
                elif type_ == tools.TypeType.Float:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetFloat();\n"
                elif type_ == tools.TypeType.Double:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetDouble();\n"
                elif type_ == tools.TypeType.Bool:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetBool();\n"
                elif type_ == tools.TypeType.String:
                    code_func += "            auto _" + _name + " = inArray[" + str(count) + "].GetString();\n"
                elif type_ == tools.TypeType.Custom:
                    code_func += "            auto _" + _name + " = " + _type + "::protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    code_func += "            std::vector<" + _array_type + "> _" + _name + ";\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code_func += "            for(auto it_" + _v_uuid + " = inArray[" + str(count) + "].Begin(); it_" + _v_uuid + " != inArray[" + str(count) + "].End(); ++it_" + _v_uuid + "){\n"
                    if array_type_ == tools.TypeType.Int32:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetInt());\n"
                    elif array_type_ == tools.TypeType.Int64:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetInt64());\n"
                    elif array_type_ == tools.TypeType.Uint32:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetUint());\n"
                    elif array_type_ == tools.TypeType.Uint64:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetUint64());\n"
                    elif array_type_ == tools.TypeType.Float:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetFloat());\n"
                    elif array_type_ == tools.TypeType.Double:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetDouble());\n"
                    elif array_type_ == tools.TypeType.Bool:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetBool());\n"
                    elif array_type_ == tools.TypeType.String:
                        code_func += "                _" + _name + ".push_back(it_" + _v_uuid + "->GetString());\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code_func += "                _" + _name + ".push_back(" + array_type + "::protcol_to_" + array_type + "(*it_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code_func += "            }\n"                                                     
                count += 1

            code_func += "            rsp = std::make_shared<" + module_name + "_" + func_name + "_rsp>(current_ch, _cb_uuid);\n"
            code_func += "            sig_" + func_name + ".emit("
            count = 0
            for _type, _name in i[2]:
                code_func += "_" + _name
                count = count + 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ");\n"
            code_func += "            rsp = nullptr;\n"
            code_func += "        }\n\n"

            rsp_code += "    class " + module_name + "_"  + func_name + "_rsp : Response {\n"
            rsp_code += "    private:\n"
            rsp_code += "        std::string uuid;\n\n"
            rsp_code += "    public:\n"
            rsp_code += "        " + module_name + "_"  + func_name + "_rsp(std::shared_ptr<Ichannel> _ch, std::string _uuid) : Response(\"" + module_name + "_rsp_cb\", _ch)\n"
            rsp_code += "        {\n"
            rsp_code += "            uuid = _uuid;\n"
            rsp_code += "        }\n\n"

            rsp_code += "        void rsp("
            for _type, _name in i[4]:
                rsp_code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[4]):
                    rsp_code += ", "
            rsp_code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            rsp_code += "            rapidjson::Document _argv_" + _argv_uuid + ";\n"
            rsp_code += "            rapidjson::Document::AllocatorType& allocator = _argv_" + _argv_uuid + ".GetAllocator();\n"
            rsp_code += "            _argv_" + _argv_uuid + ".SetArray();\n"
            rsp_code += "            rapidjson::Value str_uuid(rapidjson::kStringType);\n"
            rsp_code += "            str_uuid.SetString(uuid.c_str(), uuid.size());\n"
            rsp_code += "            _argv_" + _argv_uuid + ".PushBack(str_uuid, allocator);\n"
            for _type, _name in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_  == tools.TypeType.Int32 or type_ == tools.TypeType.Int64 or type_ == tools.TypeType.Uint32 or type_ == tools.TypeType.Uint64 or type_ == tools.TypeType.Float or type_ == tools.TypeType.Double or type_ == tools.TypeType.Bool:
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.String:
                    rsp_code += "            rapidjson::Value str_" + _name + "(rapidjson::kStringType);\n"
                    rsp_code += "            str_" + _name + ".SetString(" + _name + ".c_str(), " + _name + ".size());\n"
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(str_" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.Custom:
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(" + _type + "::" + _type + "_to_protcol(" + _name + "), allocator);\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    rsp_code += "            rapidjson::Value _array_" + _array_uuid + "(rapidjson::kArrayType);\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    rsp_code += "            for(auto v_" + _v_uuid + " : _name){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Int32 or array_type_ == tools.TypeType.Int64 or array_type_ == tools.TypeType.Uint32 or array_type_ == tools.TypeType.Uint64 or array_type_ == tools.TypeType.Float or array_type_ == tools.TypeType.Double or array_type_ == tools.TypeType.Bool:
                        rsp_code += "                _array_" + _array_uuid + ".PushBack(v_" + _v_uuid + ", allocator);\n"
                    elif type_ == tools.TypeType.String:
                        rsp_code += "                rapidjson::Value str_" + _v_uuid + "(rapidjson::kStringType);\n"
                        rsp_code += "                str_" + _v_uuid + ".SetString(v_" + _v_uuid + ".c_str(), v_" + _v_uuid + ".size());\n"
                        rsp_code += "                _array_" + _array_uuid + ".PushBack(str_" + _v_uuid + ", allocator);\n"
                    elif array_type_ == tools.TypeType.Custom:
                        rsp_code += "                _array_" + _array_uuid + ".PushBack(" + array_type + "::" + array_type + "_to_protcol(v_" + _v_uuid + "), allocator);\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    rsp_code += "            }\n"                                                     
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(_array_" + _array_uuid + ", allocator);\n"
            rsp_code += "            call_module_method(\"" + func_name + "_rsp\", _argv_" + _argv_uuid + ".GetArray());\n"
            rsp_code += "        }\n\n"

            rsp_code += "        void err("
            count = 0
            for _type, _name in i[6]:
                rsp_code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count = count + 1
                if count < len(i[6]):
                    rsp_code += ", "
            rsp_code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            rsp_code += "            rapidjson::Document _argv_" + _argv_uuid + ";\n"
            rsp_code += "            rapidjson::Document::AllocatorType& allocator = _argv_" + _argv_uuid + ".GetAllocator();\n"
            rsp_code += "            _argv_" + _argv_uuid + ".SetArray();\n"
            rsp_code += "            rapidjson::Value str_uuid(rapidjson::kStringType);\n"
            rsp_code += "            str_uuid.SetString(uuid.c_str(), uuid.size());\n"
            rsp_code += "            _argv_" + _argv_uuid + ".PushBack(str_uuid, allocator);\n"
            for _type, _name in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_  == tools.TypeType.Int32 or type_ == tools.TypeType.Int64 or type_ == tools.TypeType.Uint32 or type_ == tools.TypeType.Uint64 or type_ == tools.TypeType.Float or type_ == tools.TypeType.Double or type_ == tools.TypeType.Bool:
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.String:
                    rsp_code += "            rapidjson::Value str_" + _name + "(rapidjson::kStringType);\n"
                    rsp_code += "            str_" + _name + ".SetString(" + _name + ".c_str(), " + _name + ".size());\n"
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(str_" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.Custom:
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(" + _type + "::" + _type + "_to_protcol(" + _name + "), allocator);\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    rsp_code += "            rapidjson::Value _array_" + _array_uuid + "(rapidjson::kArrayType);\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    rsp_code += "            for(auto v_" + _v_uuid + " : _name){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Int32 or array_type_ == tools.TypeType.Int64 or array_type_ == tools.TypeType.Uint32 or array_type_ == tools.TypeType.Uint64 or array_type_ == tools.TypeType.Float or array_type_ == tools.TypeType.Double or array_type_ == tools.TypeType.Bool:
                        rsp_code += "                _array_" + _array_uuid + ".PushBack(v_" + _v_uuid + ", allocator);\n"
                    elif type_ == tools.TypeType.String:
                        rsp_code += "                rapidjson::Value str_" + _v_uuid + "(rapidjson::kStringType);\n"
                        rsp_code += "                str_" + _v_uuid + ".SetString(v_" + _v_uuid + ".c_str(), v_" + _v_uuid + ".size());\n"
                        rsp_code += "                _array_" + _array_uuid + ".PushBack(str_" + _v_uuid + ", allocator);\n"
                    elif array_type_ == tools.TypeType.Custom:
                        rsp_code += "                _array_" + _array_uuid + ".PushBack(" + array_type + "::" + array_type + "_to_protcol(v_" + _v_uuid + "), allocator);\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    rsp_code += "            }\n"                                                     
                    rsp_code += "            _argv_" + _argv_uuid + ".PushBack(_array_" + _array_uuid + ", allocator);\n"
            rsp_code += "            call_module_method(\"" + func_name + "_err\", _argv_" + _argv_uuid + ".GetArray());\n"
            rsp_code += "        }\n\n"
            rsp_code += "    };\n\n"

        else:
            raise "func:%s wrong rpc type:%s must req or ntf" % (func_name, i[1])

    code_constructor_end = "        }\n\n"
    code = "    };\n"
        
    return rsp_code + code_constructor + code_constructor_cb + code_constructor_end + code_func + code
        

def genmodule(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
        
    code = "/*this module code is codegen by abelkhan codegen for cpp*/\n"
    for module_name, funcs in modules.items():
        code += gen_module_module(module_name, funcs, dependent_struct, dependent_enum)
                
    return code