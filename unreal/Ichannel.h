/*
 * qianqians
 * 2016/7/4
 * Ichannel.h
 */
#ifndef _Ichannel_h
#define _Ichannel_h

#include "Json.h"

namespace juggle {

class Ichannel {
public:
	virtual const TSharedPtr<FJsonValue> pop() = 0;
	virtual void push(const TArray< TSharedPtr<FJsonValue> >& InArray) = 0;
	
};

}

#endif // !_Ichannel_h