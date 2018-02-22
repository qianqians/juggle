/*
 * qianqians
 * 2016/7/4
 * process.h
 */
#ifndef _process_h
#define _process_h

#include <tuple>
#include <unordered_map>
#include <set>
#include <mutex>

#include "Imodule.h"
#include "Ichannel.h"

namespace juggle {

class process {
public:
	process() {
	}

	void reg_channel(std::shared_ptr<Ichannel> ch){
		std::lock_guard<std::mutex> l(_event_set_mu);
		event_set.insert(ch);
	}

	void unreg_channel(std::shared_ptr<Ichannel> ch)
	{
		std::lock_guard<std::mutex> l(_remove_set_mu);
		if (event_set.find(ch) != event_set.end()) {
			remove_set.push_back(ch);
		}
	}

	void reg_module(std::shared_ptr<Imodule> module)
	{
		module_set.insert(std::make_pair(module->module_name, module));
	}

	void unreg_module(std::shared_ptr<Imodule> module)
	{
		module_set.erase(module->module_name);
	}


	void poll(){
		_event_set_mu.lock();
		for (auto ch : event_set) {
			while (true) {
				std::shared_ptr<std::vector<boost::any> > buff;
				if (ch->pop(buff)) {

					auto module_name = boost::any_cast<std::string>((*buff)[0]);

					auto module = module_set.find(module_name);
					if (module != module_set.end()) {
						module->second->process_event(ch, buff);
					}
					else {
						std::cout << "do not have a module named:" << module_name << std::endl;
					}
				}
				else {
					break;
				}
			}
		}
		_event_set_mu.unlock();

		_remove_set_mu.lock();
		for (auto ch : remove_set) {
			event_set.erase(ch);
		}
		remove_set.clear();
		_remove_set_mu.unlock();
	}

private:
	std::mutex _event_set_mu;
	std::set<std::shared_ptr<Ichannel> > event_set;
	
	std::mutex _remove_set_mu;
	std::vector<std::shared_ptr<Ichannel> > remove_set;

	std::unordered_map<std::string, std::shared_ptr<Imodule> > module_set;

};

}

#endif // !_process_h