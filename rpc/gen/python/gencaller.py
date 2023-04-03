#coding:utf-8
# 2020-1-21
# build by qianqians
# gencaller

import uuid
import tools

def gen_module_caller(module_name, funcs, dependent_struct, dependent_enum, enum):
    cb_func = ""

    cb_code = "#this cb code is codegen by abelkhan for python\n"
    cb_code += "class " + module_name + "_rsp_cb(Imodule):\n"
    cb_code_constructor = "    def __init__(self, modules:modulemng):\n"
    cb_code_constructor += "        super(" + module_name + "_rsp_cb, self).__init__()\n"
    cb_code_section = ""

    code = "rsp_cb_" + module_name + "_handle = None\n"
    code += "class " + module_name + "_caller(Icaller):\n"
    _uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, module_name)).split('-'))
    code += "    def __init_(self, _ch:Ichannel, modules:modulemng):\n"
    code += "        super(" + module_name + "_caller, self).__init__(_ch)\n\n"
    code += "        self.uuid_" + _uuid + " = RandomUUID()\n\n"
    code += "        global rsp_cb_" + module_name + "_handle\n"
    code += "        if not rsp_cb_" + module_name + "_handle:\n"
    code += "            rsp_cb_" + module_name + "_handle = " + module_name + "_rsp_cb(modules)\n"
    code += "\n"

    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code += "    def " + func_name + "(self, "
            count = 0
            for _type, _name, _parameter in i[2]:
                if _parameter == None:
                    code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                else:
                    code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum) + " = " + tools.convert_parameter(_type, _parameter, dependent_enum, enum)
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "):\n"
            _argv_uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, func_name)).split('-'))
            code += "        _argv_" + _argv_uuid + " = []\n"
            for _type, _name, _parameter in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ in tools.OriginalTypeList:
                    code += "        _argv_" + _argv_uuid + ".append(" + _name + ")\n"
                elif type_ == tools.TypeType.Custom:
                    code += "        _argv_" + _argv_uuid + ".append(" + _type + "_to_protcol(" + _name + "))\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, _name)).split('-'))
                    code += "        _array_" + _array_uuid + " = []\n"
                    _v_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_DNS, _name)).split('-'))
                    code += "        for v_" + _v_uuid + " in " + _name + ":\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ in tools.OriginalTypeList:
                        code += "            _array_" + _array_uuid + ".append(v_" + _v_uuid + ")\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "            _array_" + _array_uuid + ".append(" + array_type + "_to_protcol(v_" + _v_uuid + "))\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "        _argv_" + _argv_uuid + ".append(_array_" + _array_uuid + ")\n"
            code += "        self.call_module_method(\"" + module_name + "_" + func_name + "\", _argv_" + _argv_uuid + ")\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            cb_code_constructor += "        self.map_" + func_name + " = {}\n"
            
            rsp_fn = "Callable[["
            count = 0
            for _type, _name, _parameter in i[4]:
                rsp_fn += tools.convert_type(_type, dependent_struct, dependent_enum)
                count += 1
                if count < len(i[4]):
                    rsp_fn += ", "
            rsp_fn += "]]"

            err_fn = "Callable[["
            count = 0
            for _type, _name, _parameter in i[6]:
                err_fn += tools.convert_type(_type, dependent_struct, dependent_enum)
                count += 1
                if count < len(i[6]):
                    err_fn += ", "
            err_fn += "]]"

            cb_func += "class " + module_name + "_" + func_name + "_cb:\n"
            cb_func += "    def __init__(self, _cb_uuid : int, _module_rsp_cb : " + module_name + "_rsp_cb):\n"
            cb_func += "        self.cb_uuid = _cb_uuid\n"
            cb_func += "        self.module_rsp_cb = _module_rsp_cb\n"
            cb_func += "        self.event_" + func_name + "_handle_cb:" + rsp_fn + " = None\n"
            cb_func += "        self.event_" + func_name + "_handle_err:" + err_fn + " = None\n"
            cb_func += "        self.event_" + func_name + "_handle_timeout:Callable[...] = None\n\n"

            cb_func += "    def callBack(self, _cb:" + rsp_fn + ", _err:" + err_fn + "):\n"
            cb_func += "        self.event_" + func_name + "_handle_cb = _cb\n"
            cb_func += "        self.event_" + func_name + "_handle_err = _err\n"
            cb_func += "        return self\n\n"

            cb_func += "    def timeout(self, tick:int, timeout_cb:Callable[...]):\n"
            cb_func += "        t = Timer(tick, lambda : self.module_rsp_cb." + func_name + "_timeout(self.cb_uuid))\n"
            cb_func += "        t.start()\n"
            cb_func += "        self.event_" + func_name + "_handle_timeout = timeout_cb\n\n"

            cb_code_constructor += "        modules.reg_method(\"" + module_name + "_rsp_cb_" + func_name + "_rsp\", [self, self." + func_name + "_rsp])\n"
            cb_code_constructor += "        modules.reg_method(\"" + module_name + "_rsp_cb_" + func_name + "_err\", [self, self." + func_name + "_err])\n"

            cb_code_section += "    def " + func_name + "_rsp(self, inArray:list):\n"
            cb_code_section += "        uuid = inArray[0]\n"
            count = 1 
            for _type, _name, _parameter in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ in tools.OriginalTypeList:
                    cb_code_section += "        _" + _name + " = inArray[" + str(count) + "]\n"
                elif type_ == tools.TypeType.Custom:
                    cb_code_section += "        _" + _name + " = protcol_to_" + _type + "(inArray[" + str(count) + "])\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_DNS, _name)).split('-'))
                    cb_code_section += "        _" + _name + ": = []\n"
                    _v_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_X500, _name)).split('-'))
                    cb_code_section += "        for v_" + _v_uuid + " in inArray[" + str(count) + "]:\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ in tools.OriginalTypeList:
                        cb_code_section += "            _" + _name + ".append(v_" + _v_uuid + ")\n"
                    elif array_type_ == tools.TypeType.Custom:
                        cb_code_section += "            _" + _name + ".append(protcol_to_" + array_type + "(v_" + _v_uuid + "))\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                count += 1
            cb_code_section += "        rsp = self.try_get_and_del_" + func_name + "_cb(uuid)\n"
            cb_code_section += "        if rsp and rsp.event_" + func_name + "_handle_cb:\n"
            cb_code_section += "            rsp.event_" + func_name + "_handle_cb("
            count = 0
            for _type, _name, _parameter in i[4]:
                cb_code_section += "_" + _name
                count = count + 1
                if count < len(i[4]):
                    cb_code_section += ", "
            cb_code_section += ")\n\n"

            cb_code_section += "    def " + func_name + "_err(self, inArray:list):\n"
            cb_code_section += "        uuid = inArray[0]\n"
            count = 1 
            for _type, _name, _parameter in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ in tools.OriginalTypeList:
                    cb_code_section += "        _" + _name + " = inArray[" + str(count) + "]\n"
                elif type_ == tools.TypeType.Custom:
                    cb_code_section += "        _" + _name + " = protcol_to_" + _type + "(inArray[" + str(count) + "])\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_DNS, _name)).split('-'))
                    cb_code_section += "        _" + _name + ": = []\n"
                    _v_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_X500, _name)).split('-'))
                    cb_code_section += "        for v_" + _v_uuid + " in inArray[" + str(count) + "]:\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ in tools.OriginalTypeList:
                        cb_code_section += "            _" + _name + ".append(v_" + _v_uuid + ")\n"
                    elif array_type_ == tools.TypeType.Custom:
                        cb_code_section += "            _" + _name + ".append(protcol_to_" + array_type + "(v_" + _v_uuid + "))\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                count += 1
            cb_code_section += "        rsp = self.try_get_and_del_" + func_name + "_cb(uuid)\n"
            cb_code_section += "        if rsp and rsp.event_" + func_name + "_handle_err:\n"
            cb_code_section += "            rsp.event_" + func_name + "_handle_err("
            count = 0
            for _type, _name, _parameter in i[6]:
                cb_code_section += "_" + _name
                count = count + 1
                if count < len(i[6]):
                    cb_code_section += ", "
            cb_code_section += ")\n\n"

            cb_code_section += "    def " + func_name + "_timeout(self, cb_uuid : int):\n"
            cb_code_section += "        rsp = self.try_get_and_del_" + func_name + "_cb(cb_uuid)\n"
            cb_code_section += "        if rsp and rsp.event_" + func_name + "_handle_timeout:\n"
            cb_code_section += "            rsp.event_" + func_name + "_handle_timeout()\n\n"

            cb_code_section += "    def try_get_and_del_" + func_name + "_cb(self, uuid : int):\n"
            cb_code_section += "        rsp = self.map_" + func_name + ".get(uuid)\n"
            cb_code_section += "        del self.map_" + func_name + "[uuid]\n"
            cb_code_section += "        return rsp\n\n"

            _cb_uuid_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_DNS, func_name)).split('-'))
            _argv_uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, func_name)).split('-'))

            code += "    def " + func_name + "(self, "
            count = 0
            for _type, _name, _parameter in i[2]:
                if _parameter == None:
                    code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum)
                else:
                    code += _name + ":" + tools.convert_type(_type, dependent_struct, dependent_enum) + " = " + tools.convert_parameter(_type, _parameter, dependent_enum, enum)
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "):\n"
            code += "        self.uuid_" + _uuid + " = (self.uuid_" + _uuid + " + 1) & 0x7fffffff\n"
            code += "        uuid_" + _cb_uuid_uuid + " = self.uuid_" + _uuid + "\n\n"
            code += "        _argv_" + _argv_uuid + " = [uuid_" + _cb_uuid_uuid + "]\n"
            for _type, _name, _parameter in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ in tools.OriginalTypeList:
                    code += "        _argv_" + _argv_uuid + ".append(" + _name + ")\n"
                elif type_ == tools.TypeType.Custom:
                    code += "        _argv_" + _argv_uuid + ".append(" + _type + "_to_protcol(" + _name + "))\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, _name)).split('-'))
                    code += "        _array_" + _array_uuid + " = []\n"
                    _v_uuid = '_'.join(str(uuid.uuid5(uuid.NAMESPACE_X500, _name)).split('-'))
                    code += "        for v_" + _v_uuid + " in " + _name + ":\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ in tools.OriginalTypeList:
                        code += "            _array_" + _array_uuid + ".append(v_" + _v_uuid + ")\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "            _array_" + _array_uuid + ".append(" + array_type + "_to_protcol(v_" + _v_uuid + "))\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "        }\n"                                                     
                    code += "        _argv_" + _argv_uuid + ".append(_array_" + _array_uuid + ")\n"
            code += "        self.call_module_method(\"" + module_name + "_" + func_name + "\", _argv_" + _argv_uuid + ")\n\n"
            code += "        global rsp_cb_" + module_name + "_handle\n"
            code += "        cb_" + func_name + "_obj = " + module_name + "_" + func_name + "_cb(uuid_" + _cb_uuid_uuid + ", rsp_cb_" + module_name + "_handle)\n"
            code += "        if rsp_cb_" + module_name + "_handle:\n"
            code += "            rsp_cb_" + module_name + "_handle.map_" + func_name + "[uuid_" + _cb_uuid_uuid + "] = cb_" + func_name + "_obj\n"
            code += "        return cb_" + func_name + "_obj\n\n"

        else:
            raise Exception("func:" + func_name + " wrong rpc type:" + str(i[1]) + ", must req or ntf")

    cb_code_constructor += "\n"

    return cb_code + cb_code_constructor + cb_code_section + cb_func + code

def gencaller(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
    
    code = "#this caller code is codegen by abelkhan codegen for python\n"
    for module_name, funcs in modules.items():
        code += gen_module_caller(module_name, funcs, dependent_struct, dependent_enum, pretreatment.enum)
        
    return code