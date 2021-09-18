/*
 * abelkhan type 
 * qianqians
 * 2020/5/21
 */
#ifndef abelkhan_type_h_
#define abelkhan_type_h_

#include <stdarg.h>

#include <exception>
#include <string>
#include <memory>
#include <unordered_map>
#include <functional>
#include <vector>

#include <msgpack11/msgpack11.hpp>

#include <concurrent/string.h>

namespace abelkhan{

class Exception : public std::exception {
public:
    Exception(std::string _err) : std::exception() {
        err = _err;
    }

public:
    std::string err;
};

class Ichannel {
public:
    virtual void send(std::string& data) = 0;
};

class Icaller {
public:
    Icaller(std::string& _module_name, std::shared_ptr<Ichannel> _ch) {
        module_name = _module_name;
        ch = _ch;
    }
        
    void call_module_method(std::string& _method_name, msgpack11::MsgPack::array& _argv){
        msgpack11::MsgPack::array event_;
        event_.push_back(module_name);
        event_.push_back(_method_name);
        event_.push_back(_argv);
        msgpack11::MsgPack _pack(event_);
            
        ch->send(_pack.dump());
    }

protected:
    std::string module_name;

private:
    std::shared_ptr<Ichannel> ch;

};

class Response : public Icaller {
public:
    Response(std::string _module_name, std::shared_ptr<Ichannel> _ch) : Icaller(_module_name, _ch) {
    }
};

class Imodule
{
protected:
    std::unordered_map<std::string, std::function<void(const msgpack11::MsgPack::array& doc)> > events;

    public:
        Imodule(std::string _module_name) {
            module_name = _module_name;
            current_ch = nullptr;
            rsp = nullptr;
        }

        void reg_method(std::string method_name, std::function<void(const msgpack11::MsgPack::array& doc)> method) {
            events.insert(std::make_pair(method_name, method));
        }

        void process_event(std::shared_ptr<Ichannel> _ch, const msgpack11::MsgPack::array& _event)
        {
            current_ch = _ch;
            try
            {
                std::string func_name = _event[1].string_value();
                auto it_func = events.find(func_name);
                if (it_func != events.end())
                {
                    try
                    {
                        it_func->second(_event[2].array_items());
                    }
                    catch (std::exception e)
                    {
                        throw new Exception(concurrent::format("function name:%s System.Exception:%s", func_name, e.what()));
                    }
                }
                else
                {
                    throw new Exception(concurrent::format("do not have a function named:%s", func_name));
                }
            }
            catch (std::exception e)
            {
                throw new Exception(concurrent::format("System.Exception:%s", e.what()));
            }
            current_ch = nullptr;
        }

    public:
        std::shared_ptr<Ichannel> current_ch;
        std::shared_ptr<Response> rsp;
        std::string module_name;
        
    };

    class modulemng
    {
    public:
        modulemng(){
        }

        void reg_module(std::shared_ptr<Imodule> _module){
            module_set.insert(std::make_pair(_module->module_name, _module));
        }

        void unreg_module(std::shared_ptr<Imodule> _module){
            module_set.erase(_module->module_name);
        }

        void process_event(std::shared_ptr<Ichannel> _ch, const msgpack11::MsgPack::array& _event) {
            try {
                std::string module_name = _event[0].string_value();
                auto it_module = module_set.find(module_name);
                if (it_module != module_set.end()) {
                    it_module->second->process_event(_ch, _event);
                }
                else {
                    throw new Exception(concurrent::format("do not have a module named:%s", module_name));
                }
            }
            catch (std::exception e)
            {
                throw Exception(concurrent::format("System.Exception:%s", e.what()));
            }
        }

    private:
        std::map<std::string, std::shared_ptr<Imodule> > module_set;

    };
}

#endif //abelkhan_type_h_