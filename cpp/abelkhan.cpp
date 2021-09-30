/*
 * abelkhan type 
 * qianqians
 * 2021/9/19
 */
#include <chrono>
#include <random>

#include <concurrent/string_tools.h>

#include <abelkhan.h>

namespace abelkhan{

inline int64_t msec_time()
{
	auto duration = std::chrono::system_clock::now().time_since_epoch();
	return std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
}

static std::mt19937_64 e((int32_t)msec_time());
uint64_t random(){
    return e();
}

Exception::Exception(std::string _err) : std::exception() {
    err = _err;
}

Icaller::Icaller(std::string _module_name, std::shared_ptr<Ichannel> _ch) {
    module_name = _module_name;
    ch = _ch;
} 

void Icaller::call_module_method(std::string _method_name, msgpack11::MsgPack::array& _argv){
    msgpack11::MsgPack::array event_;
    event_.push_back(module_name);
    event_.push_back(_method_name);
    event_.push_back(_argv);
    msgpack11::MsgPack _pack(event_);
    auto data = _pack.dump();
            
    ch->send(data);
}

Response::Response(std::string _module_name, std::shared_ptr<Ichannel> _ch) : Icaller(_module_name, _ch) {
}

Imodule::Imodule(std::string _module_name) {
    module_name = _module_name;
    current_ch = nullptr;
    rsp = nullptr;
}

void Imodule::reg_method(std::string method_name, std::function<void(const msgpack11::MsgPack::array& doc)> method) {
    events.insert(std::make_pair(method_name, method));
}

void Imodule::process_event(std::shared_ptr<Ichannel> _ch, const msgpack11::MsgPack::array& _event)
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

modulemng::modulemng(){
}

void modulemng::reg_module(std::shared_ptr<Imodule> _module){
    module_set.insert(std::make_pair(_module->module_name, _module));
}

void modulemng::unreg_module(std::shared_ptr<Imodule> _module){
    module_set.erase(_module->module_name);
}

void modulemng::process_event(std::shared_ptr<Ichannel> _ch, const msgpack11::MsgPack::array& _event) {
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


void TinyTimer::add_timer(int64_t _tick, std::function<void()> cb){
    tick = msec_time();
    auto tick_ = _tick + tick;
    add_timer_list.push(std::make_pair(tick_, cb));
}

void TinyTimer::poll(){
    std::pair<uint64_t, std::function<void()> > timer_em;
    while(add_timer_list.pop(timer_em)){
        while(timer.find(timer_em.first) != timer.end()){
            timer_em.first++;
        }
        timer.insert(timer_em);
    }

    tick = msec_time();

    std::vector<int64_t> remove;
	for (auto it = timer.begin(); it != timer.end(); it++)
	{
		if (it->first <= tick)
		{
			it->second();
			remove.push_back(it->first);
		}
		else {
			break;
		}
	}

	for (auto key : remove)
	{
		timer.erase(key);
	}
}


}