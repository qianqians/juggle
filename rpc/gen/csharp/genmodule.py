#coding:utf-8
# 2020-1-21
# build by qianqians
# genmodule

import uuid
import tools

def gen_module_module(module_name, funcs, dependent_struct, dependent_enum):
    code_constructor = "    public class " + module_name + "_module : abelkhan.Imodule {\n"
    code_constructor += "        private abelkhan.modulemng modules;\n"
    code_constructor += "        public " + module_name + "_module(abelkhan.modulemng _modules) : base(\"" + module_name + "\")\n"
    code_constructor += "        {\n"
    code_constructor += "            modules = _modules;\n"
    code_constructor += "            modules.reg_module(this);\n\n"
        
    code_constructor_cb = ""
    rsp_code = ""
    code_func = ""
    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code_constructor += "            reg_method(\"" + func_name + "\", " + func_name + ");\n"
                
            code_func += "        public delegate void cb_" + func_name + "_handle("
            count = 0
            for _type, _name in i[2]:
                code_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count += 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ");\n"
            code_func += "        public event cb_" + func_name + "_handle on_" + func_name + ";\n\n"

            code_func += "        public void " + func_name + "(JArray inArray){\n"
            count = 0 
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code_func += "            var _" + _name + " = (" + _type_ + ")inArray[" + str(count) + "];\n"
                elif type_ == tools.TypeType.Custom:
                    code_func += "            var _" + _name + " = " + _type + ".protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    code_func += "            var _" + _name + " = new List<" + _array_type + ">();\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code_func += "            foreach(var v_" + _v_uuid + " in inArray[" + str(count) + "]){\n"
                    if array_type_ == tools.TypeType.Original:
                        code_func += "                _" + _name + ".Add((" + _array_type + ")v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code_func += "                _" + _name + ".Add(" + array_type + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code_func += "            }\n"                                                     
                count += 1

            code_func += "            if (on_" + func_name + " != null){\n"
            code_func += "                on_" + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code_func += "_" + _name
                count = count + 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ");\n"
            code_func += "            }\n"
            code_func += "        }\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            code_constructor += "            reg_method(\"" + func_name + "\", " + func_name + ");\n"
            
            code_func += "        public delegate void cb_" + func_name + "_handle("
            count = 0
            for _type, _name in i[2]:
                code_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count += 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ");\n"
            code_func += "        public event cb_" + func_name + "_handle on_" + func_name + ";\n\n"
            
            code_func += "        public void " + func_name + "(JArray inArray){\n"
            code_func += "            var _cb_uuid = (String)inArray[0];\n"
            count = 1 
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code_func += "            var _" + _name + " = (" + _type_ + ")inArray[" + str(count) + "];\n"
                elif type_ == tools.TypeType.Custom:
                    code_func += "            var _" + _name + " = " + _type + ".protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    code_func += "            var _" + _name + " = new List<" + _array_type + ">();\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code_func += "            foreach(var v_" + _v_uuid + " in inArray[" + str(count) + "]){\n"
                    if array_type_ == tools.TypeType.Original:
                        code_func += "                _" + _name + ".Add((" + _array_type + ")v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code_func += "                _" + _name + ".Add(" + array_type + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code_func += "            }\n"                                                     
                count += 1

            code_func += "            rsp = new " + module_name + "_" + func_name + "_rsp(current_ch, _cb_uuid);\n"
            code_func += "            if (on_" + func_name + " != null){\n"
            code_func += "                on_" + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code_func += "_" + _name
                count = count + 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ");\n"
            code_func += "            }\n"
            code_func += "            rsp = null;\n"
            code_func += "        }\n\n"

            rsp_code += "    public class " + module_name + "_" + func_name + "_rsp : abelkhan.Response {\n"
            rsp_code += "        private string uuid;\n"
            rsp_code += "        public " + module_name + "_" + func_name + "_rsp(abelkhan.Ichannel _ch, String _uuid) : base(\"" + module_name + "_rsp_cb\", _ch)\n"
            rsp_code += "        {\n"
            rsp_code += "            uuid = _uuid;\n"
            rsp_code += "        }\n\n"

            rsp_code += "        public void rsp("
            for _type, _name in i[4]:
                rsp_code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[4]):
                    rsp_code += ", "
            rsp_code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            rsp_code += "            var _argv_" + _argv_uuid + " = new JArray();\n"
            rsp_code += "            _argv_" + _argv_uuid + ".Add(uuid);\n"
            for _type, _name in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    rsp_code += "            _argv_" + _argv_uuid + ".Add(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    rsp_code += "            _argv_" + _argv_uuid + ".Add(" + _type + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    rsp_code += "            var _array_" + _array_uuid + " = new JArray();"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    rsp_code += "            foreach(var v_" + _v_uuid + " in " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        rsp_code += "                _array_" + _array_uuid + ".Add(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        rsp_code += "                _array_" + _array_uuid + ".Add(" + array_type + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    rsp_code += "            }\n"                                                     
                    rsp_code += "            _argv_" + _argv_uuid + ".Add(_array_" + _array_uuid + ");\n"
            rsp_code += "            call_module_method(\"" + func_name + "_rsp\", _argv_" + _argv_uuid + ");\n"
            rsp_code += "        }\n\n"

            rsp_code += "        public void err("
            count = 0
            for _type, _name in i[6]:
                rsp_code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count = count + 1
                if count < len(i[6]):
                    rsp_code += ", "
            rsp_code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            rsp_code += "            var _argv_" + _argv_uuid + " = new JArray();\n"
            rsp_code += "            _argv_" + _argv_uuid + ".Add(this.uuid);\n"
            for _type, _name in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    rsp_code += "            _argv_" + _argv_uuid + ".Add(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    rsp_code += "            _argv_" + _argv_uuid + ".Add(" + _type + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    rsp_code += "            var _array_" + _array_uuid + " = new JArray();"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    rsp_code += "            foreach(var v_" + _v_uuid + " in " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        rsp_code += "                _array_" + _array_uuid + ".Add(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        rsp_code += "                _array_" + _array_uuid + ".Add(" + array_type + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    rsp_code += "            }\n"                                                     
                    rsp_code += "            _argv_" + _argv_uuid + ".Add(_array_" + _array_uuid + ");\n"
            rsp_code += "            call_module_method(\"" + func_name + "_err\", _argv_" + _argv_uuid + ");\n"
            rsp_code += "        }\n\n"
            rsp_code += "    }\n\n"

        else:
            raise "func:%s wrong rpc type:%s must req or ntf" % (func_name, i[1])

    code_constructor_end = "        }\n\n"
    code = "    }\n"
        
    return rsp_code + code_constructor + code_constructor_cb + code_constructor_end + code_func + code
        

def genmodule(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
        
    code = "/*this module code is codegen by abelkhan codegen for c#*/\n"
    for module_name, funcs in modules.items():
        code += gen_module_module(module_name, funcs, dependent_struct, dependent_enum)
                
    return code