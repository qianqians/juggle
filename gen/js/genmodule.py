# 2018-3-16
# build by qianqians
# genmodule

def genmodule(module_name, funcs):
        code = "/*this module file is codegen by juggle for js*/\n"

        code += "function " + module_name + "_module(){\n"
        code += "    eventobj.call(this);\n"
        code += "    Imodule.call(this, \"" + module_name + "\");\n\n"

        for i in funcs:
                code += "    this." + i[1] + " = function("
                count = 0
                for item in i[2]:
                        code += "argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code += "){\n"
                code += "        this.call_event(\"" + i[1] + "\", ["
                count = 0
                for item in i[2]:
                        code += "argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code += "]);\n"
                code += "    }\n\n"
        
        code += "}\n"
        code += "(function(){\n"
        code += "    var Super = function(){};\n"
        code += "    Super.prototype = Imodule.prototype;\n"
        code += "    " + module_name + "_module.prototype = new Super();\n"
        code += "})();\n"
        code += module_name + "_module.prototype.constructor = " + module_name + "_module;\n\n";

        return code
