from abelkhan import *
from threading import Timer
from collections.abc import Callable
from enum import Enum

# this enum code is codegen by abelkhan codegen for python

class em_test3(Enum):
    enum_test3 = 1
    enum_test1 = 2
    enum_test2 = 3


#this struct code is codegen by abelkhan codegen for python
class test1(object):
    def __init__(self):
        self.argv1 = 0
        self.argv2 = "123"
        self.argv3 = 0.0
        self.argv4 = 0.0


def test1_to_protcol(_struct:test1):
    _protocol = {}
    _protocol["argv1"] = _struct.argv1
    _protocol["argv2"] = _struct.argv2
    _protocol["argv3"] = _struct.argv3
    _protocol["argv4"] = _struct.argv4
    return _protocol

def protcol_to_test1(_protocol:any):
    _struct = test1()
    for key, val in _protocol:
        if key == "argv1":
            _struct.argv1 = val
        elif key == "argv2":
            _struct.argv2 = val
        elif key == "argv3":
            _struct.argv3 = val
        elif key == "argv4":
            _struct.argv4 = val
    return _struct

class test2(object):
    def __init__(self):
        self.argv1 = 0
        self.argv2 = None
        self.bytel = bytes([1,1,9])
        self.t = em_test3.enum_test3


def test2_to_protcol(_struct:test2):
    _protocol = {}
    _protocol["argv1"] = _struct.argv1
    _protocol["argv2"] = test1_to_protcol(_struct.argv2)
    _protocol["bytel"] = _struct.bytel
    _protocol["t"] = _struct.t
    return _protocol

def protcol_to_test2(_protocol:any):
    _struct = test2()
    for key, val in _protocol:
        if key == "argv1":
            _struct.argv1 = val
        elif key == "argv2":
            _struct.argv2 = protcol_to_test1(val)
        elif key == "bytel":
            _struct.bytel = val
        elif key == "t":
            _struct.t = val
    return _struct

class test3(object):
    def __init__(self):
        self.em = em_test3.enum_test3
        self.em_list = None


def test3_to_protcol(_struct:test3):
    _protocol = {}
    _protocol["em"] = _struct.em
    if _struct.em_list:
        _array_em_list = []
        for v_ in _struct.em_list:
            _array_em_list.append(v_)
        _protocol["em_list"] = _array_em_list
    return _protocol

def protcol_to_test3(_protocol:any):
    _struct = test3()
    for key, val in _protocol:
        if key == "em":
            _struct.em = val
        elif key == "em_list":
            _struct.em_list = []
            for v_ in val:
                _struct.em_list.append(v_)
    return _struct

#this caller code is codegen by abelkhan codegen for python
#this cb code is codegen by abelkhan for python
class test_rsp_cb(Imodule):
    def __init__(self, modules:modulemng):
        super(test_rsp_cb, self).__init__()
        self.map_test3 = {}
        modules.reg_method("test_rsp_cb_test3_rsp", [self, self.test3_rsp])
        modules.reg_method("test_rsp_cb_test3_err", [self, self.test3_err])

    def test3_rsp(self, inArray:list):
        uuid = inArray[0]
        _t1 = protcol_to_test1(inArray[1])
        _i = inArray[2]
        rsp = self.try_get_and_del_test3_cb(uuid)
        if rsp and rsp.event_test3_handle_cb:
            rsp.event_test3_handle_cb(_t1, _i)

    def test3_err(self, inArray:list):
        uuid = inArray[0]
        _err = protcol_to_test1(inArray[1])
        _bytearray = inArray[2]
        rsp = self.try_get_and_del_test3_cb(uuid)
        if rsp and rsp.event_test3_handle_err:
            rsp.event_test3_handle_err(_err, _bytearray)

    def test3_timeout(self, cb_uuid : int):
        rsp = self.try_get_and_del_test3_cb(cb_uuid)
        if rsp and rsp.event_test3_handle_timeout:
            rsp.event_test3_handle_timeout()

    def try_get_and_del_test3_cb(self, uuid : int):
        rsp = self.map_test3.get(uuid)
        del self.map_test3[uuid]
        return rsp

class test_test3_cb:
    def __init__(self, _cb_uuid : int, _module_rsp_cb : test_rsp_cb):
        self.cb_uuid = _cb_uuid
        self.module_rsp_cb = _module_rsp_cb
        self.event_test3_handle_cb = None
        self.event_test3_handle_err = None
        self.event_test3_handle_timeout = None

    def callBack(self, _cb:Callable[[test1, int]], _err:Callable[[test1, bytes]]):
        self.event_test3_handle_cb = _cb
        self.event_test3_handle_err = _err
        return self

    def timeout(self, tick:int, timeout_cb:Callable[...]):
        t = Timer(tick, lambda self : self.module_rsp_cb.test3_timeout(self.cb_uuid))
        t.start()
        self.event_test3_handle_timeout = timeout_cb

rsp_cb_test_handle = None
class test_caller(Icaller):
    def __init_(self, _ch:Ichannel, modules:modulemng):
        super(test_caller, self).__init__(_ch)

        self.uuid_45a113ac_c7f2_30b0_90a5_a399ab912716 = RandomUUID()

        global rsp_cb_test_handle
        if not rsp_cb_test_handle:
            rsp_cb_test_handle = test_rsp_cb(modules)

    def test3(self, t2:test2, e:em_test3 = em_test3.enum_test3, str:str = "qianqians"):
        self.uuid_45a113ac_c7f2_30b0_90a5_a399ab912716 = (self.uuid_45a113ac_c7f2_30b0_90a5_a399ab9127161) & 0x7fffffff
        uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80 = self.uuid_45a113ac_c7f2_30b0_90a5_a399ab912716

        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = [uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80]
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(test2_to_protcol(t2))
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(e)
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(str)
        self.call_module_method("test_test3", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7)

        cb_test3_obj = test_test3_cb(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, rsp_cb_test_handle)
        global rsp_cb_test_handle
        if rsp_cb_test_handle:
            rsp_cb_test_handle.map_test3[uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80] = cb_test3_obj
        return cb_test3_obj

    def test4(self, argv:list[test2], num:float = float(0.110)):
        _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72 = []
        _array_80252816_2442_30bc_bd5c_59666cae8a23 = []
        for v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0 in argv:
            _array_80252816_2442_30bc_bd5c_59666cae8a23.append(test2_to_protcol(v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0))
        _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.append(_array_80252816_2442_30bc_bd5c_59666cae8a23)
        _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.append(num)
        self.call_module_method("test_test4", _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72)

#this module code is codegen by abelkhan codegen for python
class test_test3_rsp(Response):
    def __init__(self, _ch:Ichannel, _uuid:int):
        super(test_test3_rsp, self).__init(_ch, _uuid)
        self.uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd = _uuid

    def rsp(self, t1:test1, i:int = 110):
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = [self.uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd]
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(test1_to_protcol(t1))
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(i)
        self.call_module_method("test_rsp_cb_test3_rsp", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7)

    def err(self, err:test1, bytearray:bytes = bytes([1,1,0])):
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = [self.uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd]
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(test1_to_protcol(err))
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.append(bytearray)
        self.call_module_method("test_rsp_cb_test3_err", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7)

class test_module(Imodule):
    def __init__(self, modules:modulemng):
        super(test_module, self)
        self.modules = modules
        self.modules.reg_method("test_test3", [self, self.test3])
        self.modules.reg_method("test_test4", [self, self.test4])

        self.cb_test3 : Callable[[test2, em_test3, str]] = None
        self.cb_test4 : Callable[[list[test2], float]] = None

    def test3(self, inArray:list):
        _cb_uuid = inArray[0]
        _t2 = protcol_to_test2(inArray[1])
        _e = inArray[2]
        _str = inArray[3]
        self.rsp = test_test3_rsp(self.current_ch, _cb_uuid)
        if self.cb_test3:
            self.cb_test3(_t2, _e, _str)
        self.rsp = None

    def test4(self, inArray:list):
        _argv = []
        for v_ in inArray[0]:
            _argv.append(protcol_to_test2(v_))
        _num = inArray[1]
        if self.cb_test4:
            self.cb_test4(_argv, _num)

