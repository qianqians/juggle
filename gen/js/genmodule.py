# 2018-3-16
# build by qianqians
# genmodule

def genmodule(module_name, funcs):
        code = "/*this module file is codegen by juggle for js*/\n"

        code += "this." + module_name + "_module = function(){\n"
        code += "    Imodule.call(this, \"" + module_name + "\");\n\n"

        for i in funcs:
                code += "    this.handle_" + i[1] + " = null;\n"
                code += "    this." + i[1] + " = function("
                count = 0
                for item in i[2]:
                        code += "argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code += "){\n"
                code += "        if(this.handle_" + i[1] + " !== null){\n"
                code += "            this.handle_" + i[1] + ".call(null, "
                count = 0
                for item in i[2]:
                        code += " argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code += ");\n"
                code += "    }\n\n"
        
        code += "}\n"
        code += "(function(){\n"
        code += "var Super = function(){};\n"
        code += "Super.prototype = Imodule.prototype;\n"
        code += module_name + "_module.prototype = new Super();\n"
        code += "})();"
        code += module_name + "_module.prototype.constructor = " + module_name + "_module;\n\n";

        return code
