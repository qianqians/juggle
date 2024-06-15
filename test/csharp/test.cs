using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using MsgPack.Serialization;

namespace Abelkhan
{
/*this enum code is codegen by abelkhan codegen for c#*/

    public enum em_test3{
        enum_test3 = 1,
        enum_test1 = 2,
        enum_test2 = 3
    }
/*this struct code is codegen by abelkhan codegen for c#*/
    public class test1
    {
        public Int32 argv1;
        public string argv2 = "123";
        public float argv3;
        public double argv4;
        public static MsgPack.MessagePackObjectDictionary test1_to_protcol(test1 _struct){
            var _protocol = new MsgPack.MessagePackObjectDictionary();
            _protocol.Add("argv1", _struct.argv1);
            _protocol.Add("argv2", _struct.argv2);
            _protocol.Add("argv3", _struct.argv3);
            _protocol.Add("argv4", _struct.argv4);
            return _protocol;
        }
        public static test1 protcol_to_test1(MsgPack.MessagePackObjectDictionary _protocol){
            var _structc501822b_22a8_37ff_91a9_9545f4689a3d = new test1();
            foreach (var i in _protocol){
                if (((MsgPack.MessagePackObject)i.Key).AsString() == "argv1"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv1 = ((MsgPack.MessagePackObject)i.Value).AsInt32();
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "argv2"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv2 = ((MsgPack.MessagePackObject)i.Value).AsString();
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "argv3"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv3 = ((MsgPack.MessagePackObject)i.Value).AsSingle();
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "argv4"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv4 = ((MsgPack.MessagePackObject)i.Value).AsDouble();
                }
            }
            return _structc501822b_22a8_37ff_91a9_9545f4689a3d;
        }
    }

    public class test2
    {
        public Int32 argv1 = 0;
        public test1 argv2;
        public byte[] bytel = new byte[3]{1,1,9};
        public em_test3 t = em_test3.enum_test3;
        public static MsgPack.MessagePackObjectDictionary test2_to_protcol(test2 _struct){
            var _protocol = new MsgPack.MessagePackObjectDictionary();
            _protocol.Add("argv1", _struct.argv1);
            _protocol.Add("argv2", new MsgPack.MessagePackObject(test1.test1_to_protcol(_struct.argv2)));
            _protocol.Add("bytel", _struct.bytel);
            _protocol.Add("t", (Int32)_struct.t);
            return _protocol;
        }
        public static test2 protcol_to_test2(MsgPack.MessagePackObjectDictionary _protocol){
            var _structf1917643_06b2_3e6d_ab77_0a5044067d0a = new test2();
            foreach (var i in _protocol){
                if (((MsgPack.MessagePackObject)i.Key).AsString() == "argv1"){
                    _structf1917643_06b2_3e6d_ab77_0a5044067d0a.argv1 = ((MsgPack.MessagePackObject)i.Value).AsInt32();
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "argv2"){
                    _structf1917643_06b2_3e6d_ab77_0a5044067d0a.argv2 = test1.protcol_to_test1(((MsgPack.MessagePackObject)i.Value).AsDictionary());
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "bytel"){
                    _structf1917643_06b2_3e6d_ab77_0a5044067d0a.bytel = ((MsgPack.MessagePackObject)i.Value).AsBinary();
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "t"){
                    _structf1917643_06b2_3e6d_ab77_0a5044067d0a.t = (em_test3)((MsgPack.MessagePackObject)i.Value).AsInt32();
                }
            }
            return _structf1917643_06b2_3e6d_ab77_0a5044067d0a;
        }
    }

    public class test3
    {
        public em_test3 em = em_test3.enum_test3;
        public List<em_test3> em_list;
        public static MsgPack.MessagePackObjectDictionary test3_to_protcol(test3 _struct){
            var _protocol = new MsgPack.MessagePackObjectDictionary();
            _protocol.Add("em", (Int32)_struct.em);
            if (_struct.em_list != null) {
                var _array_em_list = new List<MsgPack.MessagePackObject>();
                foreach(var v_ in _struct.em_list){
                    _array_em_list.Add((Int32)v_);
                }
                _protocol.Add("em_list", new MsgPack.MessagePackObject(_array_em_list));
            }
            return _protocol;
        }
        public static test3 protcol_to_test3(MsgPack.MessagePackObjectDictionary _protocol){
            var _structbf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = new test3();
            foreach (var i in _protocol){
                if (((MsgPack.MessagePackObject)i.Key).AsString() == "em"){
                    _structbf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.em = (em_test3)((MsgPack.MessagePackObject)i.Value).AsInt32();
                }
                else if (((MsgPack.MessagePackObject)i.Key).AsString() == "em_list"){
                    _structbf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.em_list = new();
                    var _protocol_array = ((MsgPack.MessagePackObject)i.Value).AsList();
                    foreach (var v_ in _protocol_array){
                        _structbf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.em_list.Add((em_test3)((MsgPack.MessagePackObject)v_).AsInt32());
                    }
                }
            }
            return _structbf7f1e5a_6b28_310c_8f9e_f815dbd56fb7;
        }
    }

/*this caller code is codegen by Abelkhan codegen for c#*/
    public class test_test3_cb
    {
        private UInt64 cb_uuid;
        private test_rsp_cb module_rsp_cb;

        public test_test3_cb(UInt64 _cb_uuid, test_rsp_cb _module_rsp_cb)
        {
            cb_uuid = _cb_uuid;
            module_rsp_cb = _module_rsp_cb;
        }

        public event Action<test1, Int32> on_test3_cb;
        public event Action<test1, byte[]> on_test3_err;
        public event Action on_test3_timeout;

        public test_test3_cb callBack(Action<test1, Int32> cb, Action<test1, byte[]> err)
        {
            on_test3_cb += cb;
            on_test3_err += err;
            return this;
        }

        public void timeout(UInt64 tick, Action timeout_cb)
        {
            TinyTimer.add_timer(tick, ()=>{
                module_rsp_cb.test3_timeout(cb_uuid);
            });
            on_test3_timeout += timeout_cb;
        }

        public void call_cb(test1 t1, Int32 i)
        {
            if (on_test3_cb != null)
            {
                on_test3_cb(t1, i);
            }
        }

        public void call_err(test1 err, byte[] bytearray)
        {
            if (on_test3_err != null)
            {
                on_test3_err(err, bytearray);
            }
        }

        public void call_timeout()
        {
            if (on_test3_timeout != null)
            {
                on_test3_timeout();
            }
        }

    }

/*this cb code is codegen by Abelkhan for c#*/
    public class test_rsp_cb : Abelkhan.Imodule {
        public Dictionary<UInt64, test_test3_cb> map_test3;
        public test_rsp_cb(Abelkhan.modulemng modules) : base("test_rsp_cb")
        {
            map_test3 = new Dictionary<UInt64, test_test3_cb>();
            modules.reg_method("test_rsp_cb_test3_rsp", Tuple.Create<Abelkhan.Imodule, Action<IList<MsgPack.MessagePackObject> > >((Abelkhan.Imodule)this, test3_rsp));
            modules.reg_method("test_rsp_cb_test3_err", Tuple.Create<Abelkhan.Imodule, Action<IList<MsgPack.MessagePackObject> > >((Abelkhan.Imodule)this, test3_err));
        }

        public void test3_rsp(IList<MsgPack.MessagePackObject> inArray){
            var uuid = ((MsgPack.MessagePackObject)inArray[0]).AsUInt64();
            var _t1 = test1.protcol_to_test1(((MsgPack.MessagePackObject)inArray[1]).AsDictionary());
            var _i = ((MsgPack.MessagePackObject)inArray[2]).AsInt32();
            var rsp = try_get_and_del_test3_cb(uuid);
            if (rsp != null)
            {
                rsp.call_cb(_t1, _i);
            }
        }

        public void test3_err(IList<MsgPack.MessagePackObject> inArray){
            var uuid = ((MsgPack.MessagePackObject)inArray[0]).AsUInt64();
            var _err = test1.protcol_to_test1(((MsgPack.MessagePackObject)inArray[1]).AsDictionary());
            var _bytearray = ((MsgPack.MessagePackObject)inArray[2]).AsBinary();
            var rsp = try_get_and_del_test3_cb(uuid);
            if (rsp != null)
            {
                rsp.call_err(_err, _bytearray);
            }
        }

        public void test3_timeout(UInt64 cb_uuid){
            var rsp = try_get_and_del_test3_cb(cb_uuid);
            if (rsp != null){
                rsp.call_timeout();
            }
        }

        private test_test3_cb try_get_and_del_test3_cb(UInt64 uuid){
            lock(map_test3)
            {
                if (map_test3.TryGetValue(uuid, out test_test3_cb rsp))
                {
                    map_test3.Remove(uuid);
                }
                return rsp;
            }
        }

    }

    public class test_caller : Abelkhan.Icaller {
        public static test_rsp_cb rsp_cb_test_handle = null;
        private Int32 uuid_45a113ac_c7f2_30b0_90a5_a399ab912716 = (Int32)RandomUUID.random();

        public test_caller(Abelkhan.Ichannel _ch, Abelkhan.modulemng modules) : base("test", _ch)
        {
            if (rsp_cb_test_handle == null)
            {
                rsp_cb_test_handle = new test_rsp_cb(modules);
            }
        }

        public test_test3_cb test3(test2 t2, em_test3 e = em_test3.enum_test3, string str = "qianqians"){
            var uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80 = (UInt32)Interlocked.Increment(ref uuid_45a113ac_c7f2_30b0_90a5_a399ab912716);

            var _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = new List<MsgPack.MessagePackObject>();
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(test2.test2_to_protcol(t2));
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add((int)e);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(str);
            call_module_method("test_test3", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);

            var cb_test3_obj = new test_test3_cb(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, rsp_cb_test_handle);
            lock(rsp_cb_test_handle.map_test3)
            {
                rsp_cb_test_handle.map_test3.Add(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, cb_test3_obj);
            }
            return cb_test3_obj;
        }

        public void test4(List<test2> argv, float num = (float)0.110){
            var _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72 = new List<MsgPack.MessagePackObject>();
            var _array_80252816_2442_30bc_bd5c_59666cae8a23 = new List<MsgPack.MessagePackObject>();
            foreach(var v_264317e3_c4ab_53c4_a9a0_63d0058d8148 in argv){
                _array_80252816_2442_30bc_bd5c_59666cae8a23.Add(test2.test2_to_protcol(v_264317e3_c4ab_53c4_a9a0_63d0058d8148));
            }
            _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.Add(_array_80252816_2442_30bc_bd5c_59666cae8a23);
            _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.Add(num);
            call_module_method("test_test4", _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72);
        }

    }
/*this module code is codegen by Abelkhan codegen for c#*/
    public class test_test3_rsp : Abelkhan.Response {
        private UInt64 uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd;
        public test_test3_rsp(Abelkhan.Ichannel _ch, UInt64 _uuid) : base("test_rsp_cb", _ch)
        {
            uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd = _uuid;
        }

        public void rsp(test1 t1_ff418b5a_70ba_3756_afdf_1e2b6bdbef8c, Int32 i_72987bfb_ad8a_309a_a6ba_f222ad17c387 = 110){
            var _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = new List<MsgPack.MessagePackObject>();
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(test1.test1_to_protcol(t1_ff418b5a_70ba_3756_afdf_1e2b6bdbef8c));
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(i_72987bfb_ad8a_309a_a6ba_f222ad17c387);
            call_module_method("test_rsp_cb_test3_rsp", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
        }

        public void err(test1 err_ad2710a2_3dd2_3a8f_a4c8_a7ebbe1df696, byte[] bytearray_f6580f73_3817_3337_ac7a_6f0e34690ee8 = new byte[3]{1,1,0}){
            var _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7 = new List<MsgPack.MessagePackObject>();
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(test1.test1_to_protcol(err_ad2710a2_3dd2_3a8f_a4c8_a7ebbe1df696));
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.Add(bytearray_f6580f73_3817_3337_ac7a_6f0e34690ee8);
            call_module_method("test_rsp_cb_test3_err", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
        }

    }

    public class test_module : Abelkhan.Imodule {
        private Abelkhan.modulemng modules;
        public test_module(Abelkhan.modulemng _modules) : base("test")
        {
            modules = _modules;
            modules.reg_method("test_test3", Tuple.Create<Abelkhan.Imodule, Action<IList<MsgPack.MessagePackObject> > >((Abelkhan.Imodule)this, test3));
            modules.reg_method("test_test4", Tuple.Create<Abelkhan.Imodule, Action<IList<MsgPack.MessagePackObject> > >((Abelkhan.Imodule)this, test4));
        }

        public event Action<test2, em_test3, string> on_test3;
        public void test3(IList<MsgPack.MessagePackObject> inArray){
            var _cb_uuid = ((MsgPack.MessagePackObject)inArray[0]).AsUInt64();
            var _t2 = test2.protcol_to_test2(((MsgPack.MessagePackObject)inArray[1]).AsDictionary());
            var _e = (em_test3)((MsgPack.MessagePackObject)inArray[2]).AsInt32();
            var _str = ((MsgPack.MessagePackObject)inArray[3]).AsString();
            rsp.Value = new test_test3_rsp(current_ch.Value, _cb_uuid);
            if (on_test3 != null){
                on_test3(_t2, _e, _str);
            }
            rsp.Value = null;
        }

        public event Action<List<test2>, float> on_test4;
        public void test4(IList<MsgPack.MessagePackObject> inArray){
            var _argv = new List<test2>();
            var _protocol_arrayargv = ((MsgPack.MessagePackObject)inArray[0]).AsList();
            foreach (var v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0 in _protocol_arrayargv){
                _argv.Add(test2.protcol_to_test2(((MsgPack.MessagePackObject)v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0).AsDictionary()));
            }
            var _num = ((MsgPack.MessagePackObject)inArray[1]).AsSingle();
            if (on_test4 != null){
                on_test4(_argv, _num);
            }
        }

    }

}
