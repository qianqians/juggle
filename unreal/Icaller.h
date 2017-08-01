/*
 * qianqians
 * 2016/7/4
 * Icaller.h
 */
#ifndef _Icaller_h
#define _Icaller_h

#include "Ichannel.h"

namespace juggle {
	
class Icaller {
public:
	Icaller(TSharedPtr<Ichannel> _ch) {
		ch = _ch;
	}

protected:
	TSharedPtr<Ichannel> ch;
	FString module_name;

};

}

#endif // !_Icaller_h