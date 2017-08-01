/*
 * qianqians
 * 2016/7/4
 * process.h
 */
#ifndef _process_h
#define _process_h

#include "List.h"

#include "Imodule.h"
#include "Ichannel.h"

namespace juggle {

class process {
public:
	process() {
	}

	void reg_channel(TSharedPtr<Ichannel> ch){
		event_set.Push(ch);
	}

	void unreg_channel(TSharedPtr<Ichannel> ch)
	{
		event_set.Remove(ch);
	}

	void reg_module(TSharedPtr<Imodule> module)
	{
		module_set.Add(module->module_name, module);
	}

	void unreg_module(TSharedPtr<Imodule> module)
	{
		module_set.Remove(module->module_name);
	}


	void poll(){
		for (auto ch : event_set) {
			while (true) {
				const TSharedPtr<FJsonValue> buff = ch->pop();
				if (buff != nullptr) {
					const TArray< TSharedPtr<FJsonValue> >* _event = nullptr;
					
					if (buff->TryGetArray(_event))
					{
						auto module_name = ((*_event)[0])->AsString();

						auto module = module_set.Find(module_name);
						if (module != nullptr) {
							module->process_event(ch, _event);
						}
					}
				}
				else {
					break;
				}
			}
		}
	}

private:
	TArray<TSharedPtr<Ichannel> > event_set;
	TMap<FString, TSharedPtr<Imodule> > module_set;

};

}

#endif // !_process_h