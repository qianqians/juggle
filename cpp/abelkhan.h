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
#include <map>
#include <unordered_map>
#include <functional>
#include <vector>

#include <msgpack11/msgpack11.hpp>

#include <concurrent/string.h>
#include <concurrent/ringque.h>

namespace abelkhan{

uint64_t random();

class Exception : public std::exception {
public:
    Exception(std::string _err);

public:
    std::string err;

};

class Ichannel {
public:
    virtual void send(std::string& data) = 0;
};

class Icaller {
public:
    Icaller(std::string& _module_name, std::shared_ptr<Ichannel> _ch);
        
    void call_module_method(std::string& _method_name, msgpack11::MsgPack::array& _argv);

protected:
    std::string module_name;

private:
    std::shared_ptr<Ichannel> ch;

};

class Response : public Icaller {
public:
    Response(std::string _module_name, std::shared_ptr<Ichannel> _ch);

};

class Imodule
{
protected:
    std::unordered_map<std::string, std::function<void(const msgpack11::MsgPack::array& doc)> > events;

public:
    Imodule(std::string _module_name);

    void reg_method(std::string method_name, std::function<void(const msgpack11::MsgPack::array& doc)> method);
    void process_event(std::shared_ptr<Ichannel> _ch, const msgpack11::MsgPack::array& _event);

public:
    std::shared_ptr<Ichannel> current_ch;
    std::shared_ptr<Response> rsp;
    std::string module_name;
        
};

class modulemng
{
public:
    modulemng();

    void reg_module(std::shared_ptr<Imodule> _module);
    void unreg_module(std::shared_ptr<Imodule> _module);
    void process_event(std::shared_ptr<Ichannel> _ch, const msgpack11::MsgPack::array& _event);

private:
    std::map<std::string, std::shared_ptr<Imodule> > module_set;

};

class TinyTimer{
private:
    static int64_t tick;
    static concurrent::ringque<std::function<void()> > add_timer;
    static std::map<int64_t, std::function<void()> > timer;

public:
    static void add_timer(int64_t tick, std::function<void()> cb);
    static void poll();


};

}

#endif //abelkhan_type_h_