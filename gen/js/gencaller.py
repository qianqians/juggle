# 2018-3-16
# build by qianqians
# genmodule

def gencaller(module_name, funcs):
        code = "/*this caller file is codegen by juggle for js*/\n"

        code += "function " + module_name + "_caller(ch){\n"
        code += "    Icaller.call(this, \"" + module_name + "\", ch);\n\n"
        
        for i in funcs:
                code += "    this." + i[1] + " = function("
                count = 0
                for item in i[2]:
                        code += " argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ","
                code += "){\n"
                code += "        var _argv = ["
                for n in range(len(i[2])):
                        code += "argv" + str(n)
                        if (n+1) < len(i[2]):
                                code += ","
                code += "];\n"
                code += "        this.call_module_method.call(this, \"" + i[1] + "\", _argv);\n"
                code += "    }\n\n"

        code += "}\n"
        code += "(function(){\n"
        code += "    var Super = function(){};\n"
        code += "    Super.prototype = Icaller.prototype;\n"
        code += "    " + module_name + "_caller.prototype = new Super();\n"
        code += "})();\n"
        code += module_name + "_caller.prototype.constructor = " + module_name + "_caller;\n\n";

        return code
