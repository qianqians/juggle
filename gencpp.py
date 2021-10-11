#coding:utf-8
# 2018-3-16
# build by qianqians
# genjs

import sys
sys.path.append("./rpc/parser")
sys.path.append("./rpc/tools/cpp")
sys.path.append("./rpc/gen_common/cpp")
sys.path.append("./rpc/gen/cpp")

import uuid
import os
import jparser

import genenum
import genstruct
import gencaller
import genmodule


def gen_import(_import):
    code = "#include <abelkhan.h>\n"
    code += "#include <signals.h>\n\n"
    for _i in _import:
        code += "#include \"" + _i + ".h\"\n"
    code += "\nnamespace abelkhan\n{\n"
    return code
    
def gen(inputdir, outputdir):
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    pretreatmentdata = jparser.batch(inputdir)
    for pretreatment in pretreatmentdata:
        _uuid = '_'.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, pretreatment.name)).split('-'))
        code = "#ifndef _h_" + pretreatment.name + "_" + _uuid + "_\n"
        code += "#define _h_" + pretreatment.name + "_" + _uuid + "_\n\n"
        code += gen_import(pretreatment._import)
        code += genenum.genenum(pretreatment)
        code += genstruct.genstruct(pretreatment)
        h_code_tmp, cpp_code_tmp = gencaller.gencaller(pretreatment)
        code += h_code_tmp
        code += genmodule.genmodule(pretreatment)
        code += "\n}\n\n"
        code += "#endif //_h_" + pretreatment.name + "_" + _uuid + "_\n"

        cpp_code = "#include \"" + pretreatment.name + ".h\"\n\n"
        cpp_code += "namespace abelkhan\n{\n\n"
        cpp_code += cpp_code_tmp
        cpp_code += "\n}\n"

        file = open(outputdir + '//' + pretreatment.name + ".h", 'w')
        file.write(code)
        file.close()

        file = open(outputdir + '//' + pretreatment.name + ".cpp", 'w')
        file.write(cpp_code)
        file.close()
        
if __name__ == '__main__':
    gen(sys.argv[1], sys.argv[2])
