#coding:utf-8
# 2018-3-16
# build by qianqians
# genjs

import sys
sys.path.append("./rpc/parser")
sys.path.append("./rpc/tools/csharp")
sys.path.append("./rpc/gen_common/csharp")
sys.path.append("./rpc/gen/csharp")

import os
import jparser

import genenum
import genstruct
import gencaller
import genmodule


def gen_import(_import):
    code = "using System;\n"
    code += "using System.Collections;\n"
    code += "using System.Collections.Generic;\n"
    code += "using System.Threading;\n"
    code += "using MsgPack.Serialization;\n\n"
    code += "namespace Abelkhan\n{\n"
    return code
    
def gen(inputdir, outputdir):
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    pretreatmentdata = jparser.batch(inputdir)
    for pretreatment in pretreatmentdata:
        code = gen_import(pretreatment._import)
        code += genenum.genenum(pretreatment)
        code += genstruct.genstruct(pretreatment)
        code += gencaller.gencaller(pretreatment)
        code += genmodule.genmodule(pretreatment)
        code += "\n}\n"

        file = open(outputdir + '//' + pretreatment.name + ".cs", 'w')
        file.write(code)
        file.close()
        
if __name__ == '__main__':
    gen(sys.argv[1], sys.argv[2])
