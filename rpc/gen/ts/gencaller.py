#coding:utf-8
# 2020-1-21
# build by qianqians
# gencaller

import uuid
import tools

def gen_module_caller(module_name, funcs, dependent_struct, dependent_enum):
    cb_func = ""

    cb_code = "/*this cb code is codegen by abelkhan for ts*/\n"
    cb_code += "export class " + module_name + "_rsp_cb extends abelkhan.Imodule {\n"
    cb_code_constructor = "    constructor(modules:abelkhan.modulemng){\n"
    cb_code_constructor += "        super(\"" + module_name + "_rsp_cb\");\n"
    cb_code_constructor += "        modules.reg_module(this);\n\n"
    cb_code_section = ""

    code = "export let rsp_cb_" + module_name + "_handle : " + module_name + "_rsp_cb | null = null;\n"
    code += "export class " + module_name + "_caller extends abelkhan.Icaller {\n"
    code += "    constructor(_ch:any, modules:abelkhan.modulemng){\n"
    code += "        super(\"" + module_name + "\", _ch);\n"
    code += "        if (rsp_cb_" + module_name + "_handle == null){\n"
    code += "            rsp_cb_" + module_name + "_handle = new " + module_name + "_rsp_cb(modules);\n"
    code += "        }\n"
    code += "    }\n\n"

    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code += "    public " + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code += "        let _argv_" + _argv_uuid + ":any[] = [];\n"
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code += "        _argv_" + _argv_uuid + ".push(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        code += "        _argv_" + _argv_uuid + ".push(" + _type + "_to_protcol(" + _name + "));\n"
                    else:
                        code += "        _argv_" + _argv_uuid + ".push(" + _import + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code += "        let _array_" + _array_uuid + ":any[] = [];\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "        for(let v_" + _v_uuid + " of " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        code += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            code += "            _array_" + _array_uuid + ".push(" + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                        else:
                            code += "            _array_" + _array_uuid + ".push(" + _import + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "        }\n"                                                     
                    code += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
            code += "        this.call_module_method(\"" + func_name + "\", _argv_" + _argv_uuid + ");\n"
            code += "    }\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            rsp_fn = "("
            count = 0
            for _type, _name in i[4]:
                rsp_fn += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count += 1
                if count < len(i[4]):
                    rsp_fn += ", "
            rsp_fn += ")=>void"
            err_fn = "("
            count = 0
            for _type, _name in i[6]:
                err_fn += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count += 1
                if count < len(i[6]):
                    err_fn += ", "
            err_fn += ")=>void"

            cb_func += "export class " + module_name + "_" + func_name + "_cb{\n"
            cb_func += "    public event_" + func_name + "_handle_cb : " + rsp_fn + " | null;\n"
            cb_func += "    public event_" + func_name + "_handle_err : " + err_fn + " | null;\n"
            
            cb_func += "    constructor(){\n"
            cb_func += "        this.event_" + func_name + "_handle_cb = null;\n"
            cb_func += "        this.event_" + func_name + "_handle_err = null;\n"
            cb_func += "    }\n\n"

            cb_func += "    callBack(_cb:" + rsp_fn + ", _err:" + err_fn + ")\n    {\n"
            cb_func += "        this.event_" + func_name + "_handle_cb = _cb;\n"
            cb_func += "        this.event_" + func_name + "_handle_err = _err;\n"
            cb_func += "    }\n"
            cb_func += "}\n\n"

            cb_code += "    public map_" + func_name + ":Map<string, " + module_name + "_" + func_name + "_cb>;\n"
            cb_code_constructor += "        this.map_" + func_name + " = new Map<string, " + module_name + "_" + func_name + "_cb>();\n"
            cb_code_constructor += "        this.reg_method(\"" + func_name + "_rsp\", this." + func_name + "_rsp.bind(this));\n"
            cb_code_constructor += "        this.reg_method(\"" + func_name + "_err\", this." + func_name + "_err.bind(this));\n"

            cb_code_section += "    public " + func_name + "_rsp(inArray:any[]){\n"
            cb_code_section += "        let uuid = inArray[0];\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            cb_code_section += "        let _argv_" + _argv_uuid + ":any[] = [];\n"
            count = 1 
            for _type, _name in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    cb_code_section += "        _argv_" + _argv_uuid + ".push(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        cb_code_section += "        _argv_" + _argv_uuid + ".push(protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                    else:
                        cb_code_section += "        _argv_" + _argv_uuid + ".push(" + _import + ".protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    cb_code_section += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    cb_code_section += "        for(let v_" + _v_uuid + " of inArray[" + str(count) + "]){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        cb_code_section += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            cb_code_section += "            _array_" + _array_uuid + ".push(protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                        else:
                            cb_code_section += "            _array_" + _array_uuid + ".push(" + _import + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    cb_code_section += "        }\n"                                                     
                    cb_code_section += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
                count += 1
            cb_code_section += "        var rsp = this.map_" + func_name + ".get(uuid);\n"
            cb_code_section += "        rsp.event_" + func_name + "_handle_cb.apply(null, _argv_" + _argv_uuid + ");\n"
            cb_code_section += "        this.map_" + func_name + ".delete(uuid);\n"
            cb_code_section += "    }\n"

            cb_code_section += "    public " + func_name + "_err(inArray:any[]){\n"
            cb_code_section += "        let uuid = inArray[0];\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            cb_code_section += "        let _argv_" + _argv_uuid + ":any[] = [];\n"
            count = 1 
            for _type, _name in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    cb_code_section += "        _argv_" + _argv_uuid + ".push(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        cb_code_section += "        _argv_" + _argv_uuid + ".push(protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                    else:
                        cb_code_section += "        _argv_" + _argv_uuid + ".push(" + _import + ".protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    cb_code_section += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    cb_code_section += "        for(let v_" + _v_uuid + " of inArray[" + str(count) + "]){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        cb_code_section += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            cb_code_section += "            _array_" + _array_uuid + ".push(protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                        else:
                            cb_code_section += "            _array_" + _array_uuid + ".push(" + _import + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    cb_code_section += "        }\n"                                                     
                    cb_code_section += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
                count += 1
            cb_code_section += "        var rsp = this.map_" + func_name + ".get(uuid);\n"
            cb_code_section += "        rsp.event_" + func_name + "_handle_err.apply(null, _argv_" + _argv_uuid + ");\n"
            cb_code_section += "        this.map_" + func_name + ".delete(uuid);\n"
            cb_code_section += "    }\n"

            code += "    public " + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "){\n"
            _cb_uuid_uuid = str(uuid.uuid1())
            _cb_uuid_uuid = '_'.join(_cb_uuid_uuid.split('-'))
            code += "        let uuid_" + _cb_uuid_uuid + " = uuidv1();\n\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code += "        let _argv_" + _argv_uuid + ":any[] = [uuid_" + _cb_uuid_uuid + "];\n"
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code += "        _argv_" + _argv_uuid + ".push(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    _import = tools.get_import(_type, dependent_struct)
                    if _import == "":
                        code += "        _argv_" + _argv_uuid + ".push(" + _type + "_to_protcol(" + _name + "));\n"
                    else:
                        code += "        _argv_" + _argv_uuid + ".push(" + _import + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code += "        let _array_" + _array_uuid + ":any[] = [];"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "        for(let v_" + _v_uuid + " of " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        code += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        _import = tools.get_import(array_type, dependent_struct)
                        if _import == "":
                            code += "            _array_" + _array_uuid + ".push(" + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                        else:
                            code += "            _array_" + _array_uuid + ".push(" + _import + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "        }\n"                                                     
                    code += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
            code += "        this.call_module_method(\"" + func_name + "\", _argv_" + _argv_uuid + ");\n\n"
            code += "        let cb_" + func_name + "_obj = new " + module_name + "_" + func_name + "_cb();\n"
            code += "        if (rsp_cb_" + module_name + "_handle){\n"
            code += "            rsp_cb_" + module_name + "_handle.map_" + func_name + ".set(uuid_" + _cb_uuid_uuid + ", cb_" + func_name + "_obj);\n"
            code += "        }\n"
            code += "        return cb_" + func_name + "_obj;\n"
            code += "    }\n\n"

        else:
            raise Exception("func:" + func_name + " wrong rpc type:" + i[1] + ", must req or ntf")

    cb_code_constructor += "    }\n"
    cb_code_section += "}\n\n"
    code += "}\n"

    return cb_func + cb_code + cb_code_constructor + cb_code_section + code

def gencaller(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
    
    code = "/*this caller code is codegen by abelkhan codegen for typescript*/\n"
    for module_name, funcs in modules.items():
        code += gen_module_caller(module_name, funcs, dependent_struct, dependent_enum)
        
    return code