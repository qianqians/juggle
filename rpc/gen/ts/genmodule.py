#coding:utf-8
# 2020-1-21
# build by qianqians
# genmodule

import uuid
import tools

def gen_module_module(module_name, funcs, dependent_struct, dependent_enum):
    code_constructor = "export class " + module_name + "_module extends abelkhan.Imodule {\n"
    code_constructor += "    private modules:abelkhan.modulemng;\n"
    code_constructor += "    constructor(modules:abelkhan.modulemng){\n"
    code_constructor += "        super(\"" + module_name + "\");\n"
    code_constructor += "        this.modules = modules;\n"
    code_constructor += "        this.modules.reg_module(this);\n\n"
        
    code_constructor_cb = ""
    rsp_code = ""
    code_func = ""
    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code_constructor += "        this.reg_method(\"" + func_name + "\", this." + func_name + ".bind(this));\n"
            code_constructor_cb += "        this.cb_" + func_name + " = null;\n\n"
                
            code_func += "    public cb_" + func_name + " : ("
            count = 0
            for _type, _name in i[2]:
                code_func += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count += 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ")=>void | null;\n"

            code_func += "    " + func_name + "(inArray:any[]){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code_func += "        let _argv_" + _argv_uuid + ":any[] = [];\n"
            count = 0 
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code_func += "        _argv_" + _argv_uuid + ".push(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        code_func += "        _argv_" + _argv_uuid + ".push(protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                    else:
                        code_func += "        _argv_" + _argv_uuid + ".push(" + _import + ".protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code_func += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code_func += "        for(let v_" + _v_uuid + " of inArray[" + str(count) + "]){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        code_func += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            code_func += "            _array_" + _array_uuid + ".push(protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                        else:
                            code_func += "            _array_" + _array_uuid + ".push(" + _import + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code_func += "        }\n"                                                     
                    code_func += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
                count += 1

            code_func += "        if (this.cb_" + func_name + "){\n"
            code_func += "            this.cb_" + func_name + ".apply(null, _argv_" + _argv_uuid + ");\n"
            code_func += "        }\n"
            code_func += "    }\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            code_constructor += "        this.reg_method(\"" + func_name + "\", this." + func_name + ".bind(this));\n"
            code_constructor_cb += "        this.cb_" + func_name + " = null;\n\n"

            code_func += "    public cb_" + func_name + " : ("
            count = 0
            for _type, _name in i[2]:
                code_func += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count += 1
                if count < len(i[2]):
                    code_func += ", "
            code_func += ")=>void | null;\n"

            code_func += "    " + func_name + "(inArray:any[]){\n"
            code_func += "        let _cb_uuid = inArray[0];\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code_func += "        let _argv_" + _argv_uuid + ":any[] = [];\n"
            count = 1 
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code_func += "        _argv_" + _argv_uuid + ".push(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        code_func += "        _argv_" + _argv_uuid + ".push(protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                    else:
                        code_func += "        _argv_" + _argv_uuid + ".push(" + _import + ".protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code_func += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code_func += "        for(let v_" + _v_uuid + " of inArray[" + str(count) + "]){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        code_func += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            code_func += "            _array_" + _array_uuid + ".push(protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                        else:
                            code_func += "            _array_" + _array_uuid + ".push(" + _import + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code_func += "        }\n"                                                     
                    code_func += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
                count += 1

            code_func += "        this.rsp = new " + module_name + "_" + func_name + "_rsp(this.current_ch, _cb_uuid);\n"
            code_func += "        if (this.cb_" + func_name + "){\n"
            code_func += "            this.cb_" + func_name + ".apply(null, _argv_" + _argv_uuid + ");\n"
            code_func += "        }\n"
            code_func += "        this.rsp = null;\n"
            code_func += "    }\n\n"

            rsp_code += "export class " + module_name + "_" + func_name + "_rsp extends abelkhan.Icaller {\n"
            rsp_code += "    private uuid : string;\n"
            rsp_code += "    constructor(_ch:any, _uuid:string){\n"
            rsp_code += "        super(\"" + module_name + "_rsp_cb\", _ch);\n"
            rsp_code += "        this.uuid = _uuid;\n"
            rsp_code += "    }\n\n"

            rsp_code += "    public rsp("
            for _type, _name in i[4]:
                rsp_code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count = count + 1
                if count < len(i[4]):
                    rsp_code += ", "
            rsp_code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            rsp_code += "        let _argv_" + _argv_uuid + ":any[] = [this.uuid];\n"
            for _type, _name in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    rsp_code += "        _argv_" + _argv_uuid + ".push(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        rsp_code += "        _argv_" + _argv_uuid + ".push(" + _type + "_to_protcol(" + _name + "));\n"
                    else:
                        rsp_code += "        _argv_" + _argv_uuid + ".push(" + _import + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    rsp_code += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    rsp_code += "        for(let v_" + _v_uuid + " of " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        rsp_code += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            rsp_code += "            _array_" + _array_uuid + ".push(" + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                        else:
                            rsp_code += "            _array_" + _array_uuid + ".push(" + _import + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    rsp_code += "        }\n"                                                     
                    rsp_code += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
            rsp_code += "        this.call_module_method(\"" + func_name + "_rsp\", _argv_" + _argv_uuid + ");\n"
            rsp_code += "    }\n\n"

            rsp_code += "    public err("
            count = 0
            for _type, _name in i[6]:
                rsp_code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count = count + 1
                if count < len(i[6]):
                    rsp_code += ", "
            rsp_code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            rsp_code += "        let _argv_" + _argv_uuid + ":any[] = [this.uuid];\n"
            for _type, _name in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    rsp_code += "        _argv_" + _argv_uuid + ".push(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        rsp_code += "        _argv_" + _argv_uuid + ".push(" + _type + "_to_protcol(" + _name + "));\n"
                    else:
                        rsp_code += "        _argv_" + _argv_uuid + ".push(" + _import + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    rsp_code += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    rsp_code += "        for(let v_" + _v_uuid + " of " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        rsp_code += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            rsp_code += "            _array_" + _array_uuid + ".push(" + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                        else:
                            rsp_code += "            _array_" + _array_uuid + ".push(" + _import + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    rsp_code += "        }\n"                                                     
                    rsp_code += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
            rsp_code += "        this.call_module_method(\"" + func_name + "_err\", _argv_" + _argv_uuid + ");\n"
            rsp_code += "    }\n\n"
            rsp_code += "}\n\n"

        else:
            raise "func:%s wrong rpc type:%s must req or ntf" % (func_name, i[1])

    code_constructor_end = "    }\n\n"
    code = "}\n"
        
    return rsp_code + code_constructor + code_constructor_cb + code_constructor_end + code_func + code
        

def genmodule(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
        
    code = "/*this module code is codegen by abelkhan codegen for typescript*/\n"
    for module_name, funcs in modules.items():
        code += gen_module_module(module_name, funcs, dependent_struct, dependent_enum)
                
    return code