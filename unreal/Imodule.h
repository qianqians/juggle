/*
 * qianqians
 * 2016/7/4
 * Imodule.h
 */
#ifndef _Imodule_h
#define _Imodule_h

#include "Map.h"

#include "Ichannel.h"

namespace juggle {

extern TSharedPtr<Ichannel> current_ch;

class Imodule {
public:
	void process_event(TSharedPtr<Ichannel> _ch, const TArray< TSharedPtr<FJsonValue> >* _event) {
		current_ch = _ch;

		auto func_name = ((*_event)[1])->AsString();
		auto func = protcolcall_set.Find(func_name);
		if (func != nullptr) {
			func(this, ((*_event)[2])->AsArray());
		}

		current_ch = nullptr;
	}

public:
	FString module_name;

protected:
	typedef void(*callback)(const TArray< TSharedPtr<FJsonValue> >& InArray);
	TMap<FString, callback> > protcolcall_set;

};

}

#endif // !_Imodule_h
