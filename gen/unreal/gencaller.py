# 2016-7-1
# build by qianqians
# gencaller

import tools

def gencaller(module_name, funcs):
        code = "/*this caller file is codegen by juggle for c++*/\n"
        code += "#ifndef _" + module_name + "_caller_h\n"
        code += "#define _" + module_name + "_caller_h\n\n"
		
        code += "#include \"Icaller.h\"\n"
        code += "#include \"Ichannel.h\"\n\n"

        code += "namespace caller\n"
        code += "{\n"
        code += "class " + module_name + " : public juggle::Icaller {\n"
        code += "public:\n"
        code += "    " + module_name + "(TSharedPtr<juggle::Ichannel> _ch) : Icaller(_ch) {\n"
        code += "        module_name = \"" + module_name + "\";\n"
        code += "    }\n\n"

        code += "    ~" + module_name + "(){\n"
        code += "    }\n\n"

        for i in funcs:
                code += "    void " + i[1] + "("
                count = 0
                for item in i[2]:
                        code += tools.gentypetocpp(item) + " argv" + str(count)
                        count = count + 1
                        if count < len(i[2]):
                                code += ","
                code += "){\n"
                code += "        TArray< TSharedPtr<FJsonValue> > v;\n"
                code += "        v.Push(TSharedPtr<FJsonValue>(new FJsonValueString(\"" + module_name + "\")));\n"
                code += "        v.Push(TSharedPtr<FJsonValue>(new FJsonValueString(\"" + i[1] + "\")));\n"
                code += "        v.Push(TSharedPtr<FJsonValue>(new FJsonValueArray(TArray< TSharedPtr<FJsonValue> >()));\n"
                for count in range(len(i[2])):
                        code += "        (v[2])->AsArray().Push(TSharedPtr<FJsonValue>(new " + tools.genjsonvaluetypefromunreal(i[2][count]) + "(argv" + str(count) + ")));\n"
                code += "        ch->push(v);\n"
                code += "    }\n\n"

        code += "};\n\n"
        code += "}\n\n"
        code += "#endif\n"

        return code
