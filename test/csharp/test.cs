using System;
using Newtonsoft.Json.Linq;

namespace abelkhan
{
/*this enum code is codegen by abelkhan codegen for c#*/

/*this struct code is codegen by abelkhan codegen for c#*/
    public class test1
    {
        public Int32 argv1;
        public String argv2;
        public Single argv3;
        public Double argv4;

        public test1(Int32 _argv1, String _argv2, Single _argv3, Double _argv4){
            argv1 = _argv1;
            argv2 = _argv2;
            argv3 = _argv3;
            argv4 = _argv4;
        }
        public static JArray test1_to_protcol(test1 _struct){
            var _protocol = new JArray();
            _protocol.Add(_struct.argv1);
            _protocol.Add(_struct.argv2);
            _protocol.Add(_struct.argv3);
            _protocol.Add(_struct.argv4);
            return _protocol;
        }
        public static test1 protcol_to_test1(JArray _protocol){
            var _argv1 = (Int32)_protocol[0];
            var _argv2 = (String)_protocol[1];
            var _argv3 = (Single)_protocol[2];
            var _argv4 = (Double)_protocol[3];
            var _struct = new test1(_argv1,_argv2,_argv3,_argv4);
            return _struct;
        }
    }

    public class test2
    {
        public Int32 argv1;
        public test1 argv2;

        public test2(Int32 _argv1, test1 _argv2){
            argv1 = _argv1;
            argv2 = _argv2;
        }
        public static JArray test2_to_protcol(test2 _struct){
            var _protocol = new JArray();
            _protocol.Add(_struct.argv1);
            _protocol.Add(test1.test1_to_protcol(_struct.argv2));
            return _protocol;
        }
        public static test2 protcol_to_test2(JArray _protocol){
            var _argv1 = (Int32)_protocol[0];
            var _argv2 = test1.protcol_to_test1(_protocol[1]);
            var _struct = new test2(_argv1,_argv2);
            return _struct;
        }
    }

/*this caller code is codegen by abelkhan codegen for c#*/
    public class test_test3_cb
    {
        public delegate void test3_handle_cb(test1 t1);
        public event test3_handle_cb ontest3_cb;

        public delegate void test3_handle_err(Int32 err);
        public event test3_handle_err ontest3_err;

        public void callBack(test3_handle_cb cb, test3_handle_err err)
        {
            ontest3_cb += cb;
            ontest3_err += err;
        }

        public void call_cb(test1 t1)
        {
            if (ontest3_cb != null)
            {
                ontest3_cb(t1);
            }
        }

        public void call_err(Int32 err)
        {
            if (ontest3_err != null)
            {
                ontest3_err(err);
            }
        }

    }

/*this cb code is codegen by abelkhan for c#*/
    public class test_rsp_cb : abelkhan.Imodule {
        public Dictionary<string, test_test3_cb> map_test3;
        public test_rsp_cb(abelkhan.modulemng modules) : base("test_rsp_cb")
        {
            modules.reg_module(this);

            map_test3 = new Dictionary<string, test_test3_cb>();
            reg_method("test3_rsp", test3_rsp);
            reg_method("test3_err", test3_err);
        }
        public void test3_rsp(JArray inArray){
            var uuid = (String)inArray[0];
            var _t1 = test1.protcol_to_test1(inArray[1]);
            var rsp = map_test3[uuid];
            rsp.call_cb(_t1);
            map_test3.Remove(uuid);
        }
        public void test3_err(JArray inArray){
            var uuid = (String)inArray[0];
            var _err = (Int32)inArray[1];
            var rsp = map_test3[uuid];
            rsp.call_err(_err);
            map_test3.Remove(uuid);
        }
    }

    public class test_caller : abelkhan.Icaller {
        public static test_rsp_cb rsp_cb_test_handle = null;
        public test_caller(abelkhan.Ichannel _ch, abelkhan.modulemng modules) : base("test", _ch)
        {
            if (rsp_cb_test_handle == null)
            {
                rsp_cb_test_handle = new rsp_cb_test(modules);
            }
        }

        public test_test3_cb test3(test2 t2){
            var uuid_6a9bce30_b45f_11ea_845b_a85e451255ad = System.Guid.NewGuid().ToString("N");

            var _argv_6a9c6a70_b45f_11ea_9c28_a85e451255ad = new JArray();
            _argv_6a9c6a70_b45f_11ea_9c28_a85e451255ad.Add(uuid_6a9bce30_b45f_11ea_845b_a85e451255ad);
            _argv_6a9c6a70_b45f_11ea_9c28_a85e451255ad.Add(test2.test2_to_protcol(t2));
            call_module_method("test3", _argv_6a9c6a70_b45f_11ea_9c28_a85e451255ad);

            var cb_test3_obj = new test_test3_cb();
            rsp_cb_test_handle.map_test3.Add(uuid_6a9bce30_b45f_11ea_845b_a85e451255ad, cb_test3_obj);
            return cb_test3_obj;
        }

        public void test4(List<test2> argv){
            var _argv_6a9c6a71_b45f_11ea_94d6_a85e451255ad = new JArray();
            var _array_6a9c6a72_b45f_11ea_a45e_a85e451255ad = new JArray();
            foreach(var v_6a9c6a73_b45f_11ea_8023_a85e451255ad in argv){
                _array_6a9c6a72_b45f_11ea_a45e_a85e451255ad.Add(test2.test2_to_protcol(v_6a9c6a73_b45f_11ea_8023_a85e451255ad));
            }
            _argv_6a9c6a71_b45f_11ea_94d6_a85e451255ad.Add(_array_6a9c6a72_b45f_11ea_a45e_a85e451255ad);
            call_module_method("test4", _argv_6a9c6a71_b45f_11ea_94d6_a85e451255ad);
        }

    }
/*this module code is codegen by abelkhan codegen for c#*/
    public class test_test3_rsp : abelkhan.Response {
        private string uuid;
        public test_test3_rsp(abelkhan.Ichannel _ch, String _uuid) : base("test_rsp_cb", _ch)
        {
            uuid = _uuid;
        }

        public void rsp(test1 t1){
            var _argv_6a9c6a74_b45f_11ea_8a38_a85e451255ad = new JArray();
            _argv_6a9c6a74_b45f_11ea_8a38_a85e451255ad.Add(uuid);
            _argv_6a9c6a74_b45f_11ea_8a38_a85e451255ad.Add(test1.test1_to_protcol(t1));
            call_module_method("test3_rsp", _argv_6a9c6a74_b45f_11ea_8a38_a85e451255ad);
        }

        public void err(Int32 err){
            var _argv_6a9c6a75_b45f_11ea_b636_a85e451255ad = new JArray();
            _argv_6a9c6a75_b45f_11ea_b636_a85e451255ad.Add(this.uuid);
            _argv_6a9c6a75_b45f_11ea_b636_a85e451255ad.Add(err);
            call_module_method("test3_err", _argv_6a9c6a75_b45f_11ea_b636_a85e451255ad);
        }

    }

    public class test_module : abelkhan.Imodule {
        private abelkhan.modulemng modules;
        public test_module(abelkhan.modulemng _modules) : base("test")
        {
            modules = _modules;
            modules.reg_module(this);

            reg_method("test3", test3);
            reg_method("test4", test4);
        }

        public delegate void cb_test3_handle(test2 t2);
        public event cb_test3_handle on_test3;

        public void test3(JArray inArray){
            var _cb_uuid = (String)inArray[0];
            var _t2 = test2.protcol_to_test2(inArray[1]);
            rsp = new test_test3_rsp(current_ch, _cb_uuid);
            if (on_test3 != null){
                on_test3(_t2);
            }
            rsp = null;
        }

        public delegate void cb_test4_handle(List<test2> argv);
        public event cb_test4_handle on_test4;

        public void test4(JArray inArray){
            var _argv = new List<test2>();
            foreach(var v_6a9c6a76_b45f_11ea_9a9e_a85e451255ad in inArray[0]){
                _argv.Add(test2.protcol_to_test2(v_6a9c6a76_b45f_11ea_9a9e_a85e451255ad));
            }
            if (on_test4 != null){
                on_test4(_argv);
            }
        }

    }

}
