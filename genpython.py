#coding:utf-8
# 2018-3-16
# build by qianqians
# genjs

import sys
sys.path.append("./rpc/parser")
sys.path.append("./rpc/tools/python")
sys.path.append("./rpc/gen_common/python")
sys.path.append("./rpc/gen/python")

import os
import jparser

import genenum
import genstruct
import gencaller
import genmodule

def gen_import(_import):
    code = "from abelkhan import *\n"
    code += "from enum import Enum\n\n"
    for _i in _import:
        code += "from" + _i + " import *\n"
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

        file = open(outputdir + '//' + pretreatment.name + ".py", 'w')
        file.write(code)
        file.close()

if __name__ == '__main__':
        gen(sys.argv[1], sys.argv[2])
