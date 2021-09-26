#ifndef _h_test_45a113ac_c7f2_30b0_90a5_a399ab912716_
#define _h_test_45a113ac_c7f2_30b0_90a5_a399ab912716_

#include <abelkhan.h>
#include <signals.h>

namespace abelkhan
{
/*this enum code is codegen by abelkhan codegen for cpp*/

/*this struct code is codegen by abelkhan codegen for cpp*/
    class test1 {
    public:
        int32_t argv1;
        std::string argv2 = "123";
        float argv3;
        double argv4;

    public:
        test1() = default;
        test1(test1& value) = default;

    public:
        static msgpack11::MsgPack::object test1_to_protcol(test1 _struct){
            msgpack11::MsgPack::object _protocol;
            _protocol.insert(std::make_pair("argv1", _struct.argv1));
            _protocol.insert(std::make_pair("argv2", _struct.argv2));
            _protocol.insert(std::make_pair("argv3", _struct.argv3));
            _protocol.insert(std::make_pair("argv4", _struct.argv4));
            return _protocol;
        }
        static test1 protcol_to_test1(const msgpack11::MsgPack::object& _protocol){
            test1 _structc501822b_22a8_37ff_91a9_9545f4689a3d;
            for(auto i : _protocol){
                if (i.first == "argv1"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv1 = i.second.int32_value();
                }
                else if (i.first == "argv2"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv2 = i.second.string_value();
                }
                else if (i.first == "argv3"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv3 = i.second.float32_value();
                }
                else if (i.first == "argv4"){
                    _structc501822b_22a8_37ff_91a9_9545f4689a3d.argv4 = i.second.float64_value();
                }
            }
            return _structc501822b_22a8_37ff_91a9_9545f4689a3d;
        }
    };

    class test2 {
    public:
        int32_t argv1 = 0;
        test1 argv2;

    public:
        test2() = default;
        test2(test2& value) = default;

    public:
        static msgpack11::MsgPack::object test2_to_protcol(test2 _struct){
            msgpack11::MsgPack::object _protocol;
            _protocol.insert(std::make_pair("argv1", _struct.argv1));
            _protocol.insert(std::make_pair("argv2", test1::test1_to_protcol(_struct.argv2)));
            return _protocol;
        }
        static test2 protcol_to_test2(const msgpack11::MsgPack::object& _protocol){
            test2 _structf1917643_06b2_3e6d_ab77_0a5044067d0a;
            for(auto i : _protocol){
                if (i.first == "argv1"){
                    _structf1917643_06b2_3e6d_ab77_0a5044067d0a.argv1 = i.second.int32_value();
                }
                else if (i.first == "argv2"){
                    _structf1917643_06b2_3e6d_ab77_0a5044067d0a.argv2 = test1::protcol_to_test1(i.second.object_items());
                }
            }
            return _structf1917643_06b2_3e6d_ab77_0a5044067d0a;
        }
    };

/*this caller code is codegen by abelkhan codegen for cpp*/
    class test_test3_cb : public std::enable_shared_from_this<test_test3_cb>{
    private:
        uint64_t cb_uuid;
        std::shared_ptr<test_rsp_cb> module_rsp_cb;

    public:
        test_test3_cb(uint64_t _cb_uuid, std::shared_ptr<test_rsp_cb> _module_rsp_cb){
            cb_uuid = _cb_uuid;
            module_rsp_cb = _module_rsp_cb;
        }

    public:
        concurrent::signals<void(test1 t1, int32_t i)> sig_test3_cb;
        concurrent::signals<void(test1 err, std::vector<uint8_t> bytearray)> sig_test3_err;
        concurrent::signals<void()> sig_test3_timeout;

        std::shared_ptr<test_test3_cb> callBack(std::function<void(test1 t1, int32_t i)> cb, std::function<void(test1 err, std::vector<uint8_t> bytearray)> err)
        {
            sig_test3_cb.connect(cb);
            sig_test3_err.connect(err);
            return shared_from_this();
        }

        void timeout(uint64_t tick, std::function<void()> timeout_cb)
        {
            TinyTimer::add_timer(tick, [this](){
                module_rsp_cb->test3_timeout(cb_uuid);
            });
            sig_test3_timeout.connect(timeout_cb);
        }

    };

/*this cb code is codegen by abelkhan for cpp*/
    class test_rsp_cb : public Imodule, public std::enable_shared_from_this<test_rsp_cb>{
    public:
        std::mutex mutex_map_test3;
        std::map<uint64_t, std::shared_ptr<test_test3_cb> > map_test3;
        test_rsp_cb() : Imodule("test_rsp_cb")
        {
        }

        void Init(std::shared_ptr<modulemng> modules){
            modules->reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));

            reg_method("test3_rsp", std::bind(&test_rsp_cb::test3_rsp, this, std::placeholders::_1));
            reg_method("test3_err", std::bind(&test_rsp_cb::test3_err, this, std::placeholders::_1));
        }
        void test3_rsp(const msgpack11::MsgPack::array& inArray){
            auto uuid = inArray[0].uint64_value();
            auto _t1 = test1::protcol_to_test1(inArray[1].object_items());
            auto _i = inArray[2].int32_value();
            auto rsp = try_get_and_del_test3_cb(uuid);
            if (rsp != nullptr){
                rsp->sig_test3_cb.emit(_t1, _i);
            }
        }
        void test3_err(const msgpack11::MsgPack::array& inArray){
            auto uuid = inArray[0].uint64_value();
            auto _err = test1::protcol_to_test1(inArray[1].object_items());
            auto _bytearray = inArray[2].binary_items();
            auto rsp = try_get_and_del_test3_cb(uuid);
            if (rsp != nullptr){
                rsp->sig_test3_err.emit(_err, _bytearray);
            }
        }

        void test3_timeout(uint64_t cb_uuid){
            auto rsp = try_get_and_del_test3_cb(cb_uuid);
            if (rsp != nullptr){
                rsp->sig_test3_timeout.emit();
            }
        }

        std::shared_ptr<test_test3_cb> try_get_and_del_test3_cb(uint64_t uuid){
            std::lock_guard<std::mutex> l(mutex_map_test3);
            auto rsp = map_test3[uuid];
            map_test3.erase(uuid);
            return rsp;
        }

    };

    class test_caller : Icaller {
    private:
        static std::shared_ptr<test_rsp_cb> rsp_cb_test_handle;

    private:
        std::atomic<uint64_t> uuid;

    public:
        test_caller(std::shared_ptr<Ichannel> _ch, std::shared_ptr<modulemng> modules) : Icaller("test", _ch)
        {
            if (rsp_cb_test_handle == nullptr){
                rsp_cb_test_handle = std::make_shared<test_rsp_cb>();
                rsp_cb_test_handle->Init(modules);
            }
            uuid.store(random());
        }

        std::shared_ptr<test_test3_cb> test3(test2 t2, std::string str = "qianqians"){
            auto uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80 = uuid++;
            msgpack11::MsgPack::array _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7;
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(test2::test2_to_protcol(t2));
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(str);
            call_module_method("test3", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);

            auto cb_test3_obj = std::make_shared<test_test3_cb>(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, rsp_cb_test_handle);
            std::lock_guard<std::mutex> l(rsp_cb_test_handle->mutex_map_test3);
            rsp_cb_test_handle->map_test3.insert(std::make_pair(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, cb_test3_obj));
            return cb_test3_obj;
        }

        void test4(std::vector<test2> argv, float num = (float)0.110){
            msgpack11::MsgPack::array _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72;
            msgpack11::MsgPack::array _array_80252816_2442_30bc_bd5c_59666cae8a23;
            for(auto v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0 : argv){
                _array_80252816_2442_30bc_bd5c_59666cae8a23.push_back(test2::test2_to_protcol(v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0));
            }
            _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.push_back(_array_80252816_2442_30bc_bd5c_59666cae8a23);
            _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.push_back(num);
            call_module_method("test4", _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72);
        }

    };
/*this module code is codegen by abelkhan codegen for cpp*/
    class test_test3_rsp : Response {
    private:
        uint64_t uuid;

    public:
        test_test3_rsp(std::shared_ptr<Ichannel> _ch, uint64_t _uuid) : Response("test_rsp_cb", _ch)
        {
            uuid = _uuid;
        }

        void rsp(test1 t1, int32_t i = 110){
            msgpack11::MsgPack::array _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7;
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(uuid);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(test1::test1_to_protcol(t1));
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(i);
            call_module_method("test3_rsp", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
        }

        void err(test1 err, std::vector<uint8_t> bytearray = {1,1,0}){
            msgpack11::MsgPack::array _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7;
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(uuid);
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(test1::test1_to_protcol(err));
            _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push_back(bytearray);
            call_module_method("test3_err", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
        }

    };

    class test_module : Imodule, public std::enable_shared_from_this<test_module>{
    public:
        test_module() : Imodule("test")
        {
        }

        void Init(std::shared_ptr<modulemng> _modules){
            _modules->reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));

            reg_method("test3", std::bind(&test_module::test3, this, std::placeholders::_1));
            reg_method("test4", std::bind(&test_module::test4, this, std::placeholders::_1));
        }

        concurrent::signals<void(test2 t2, std::string str)> sig_test3;
        void test3(const msgpack11::MsgPack::array& inArray){
            auto _cb_uuid = inArray[0].uint64_value();
            auto _t2 = test2::protcol_to_test2(inArray[1].object_items());
            auto _str = inArray[2].string_value();
            rsp = std::make_shared<test_test3_rsp>(current_ch, _cb_uuid);
            sig_test3.emit(_t2, _str);
            rsp = nullptr;
        }

        concurrent::signals<void(std::vector<test2> argv, float num)> sig_test4;
        void test4(const msgpack11::MsgPack::array& inArray){
            std::vector<test2> _argv;
            auto _protocol_array = inArray[0].array_items();
            for(auto it_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0 : _protocol_array){
                _argv.push_back(test2::protcol_to_test2(it_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0.object_items()));
            }
            auto _num = inArray[1].float32_value();
            sig_test4.emit(_argv, _num);
        }

    };

}

#endif //_h_test_45a113ac_c7f2_30b0_90a5_a399ab912716_
