# 2016-7-1
# build by qianqians
# genmodule

import tools

def genmodule(module_name, funcs):
        code = "/*this module file is codegen by juggle for c++*/\n"
        code += "#ifndef _" + module_name + "_module_h\n"
        code += "#define _" + module_name + "_module_h\n\n"
        code += "#include \"Imodule.h\"\n\n"

        code += "namespace module\n{\n"
        code += "class " + module_name + " : public juggle::Imodule {\n"
        code += "public:\n"
        code += "    " + module_name + "(){\n"
        code += "        module_name = \"" + module_name + "\";\n"
        for i in funcs:
                code += "        protcolcall_set.Add(\"" + i[1] + "_handle\", &" + module_name + "::" + i[1] + "_handle);\n"

        code += "    }\n\n"

        code += "    ~" + module_name + "(){\n"
        code += "    }\n\n"

        for i in funcs:
                code += "    virtual void" + i[1] + "("
                count = 0
                for item in i[2]:
                        code += tools.gentypetocpp(item) + " argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code += ");\n"
                code += "    void " + i[1] + "_handle(const TArray< TSharedPtr<FJsonValue> >& _event){\n"
				count = 0
				for item in i[2]:
						code += "		" + tools.gentypetocpp(item) + " argv" + str(count) + " = nullptr;\n"
						code += "		if ( !(_event[" + str(count) + "])->" + tools.gengetargvfromunreal(item) + "(argv" + str(count) + ") ){\n"
						code += "			return;\n		}\n"
						count = count + 1
                code += "       " + i[1] + "(\n"
                count = 0
                for item in i[2]:
                        code += "            argv" + str(count)
                        count += 1
                        if count < len(i[2]):
                                code += ", "
                code += ");\n"
                code += "    }\n\n"

        code += "};\n\n"
        code += "}\n\n"
        code += "#endif\n"

        return code
