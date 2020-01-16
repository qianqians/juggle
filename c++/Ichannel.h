/*
 * qianqians
 * 2016/7/4
 * Ichannel.h
 */
#ifndef _Ichannel_h
#define _Ichannel_h

#include <vector>
#include <memory>

#include <JsonParse.h>

namespace juggle {

class Ichannel {
public:
	virtual void disconnect() = 0;
	virtual bool pop(Fossilizid::JsonParse::JsonArray  &) = 0;
	virtual void push(Fossilizid::JsonParse::JsonArray ) = 0;
	
};

}

#endif // !_Ichannel_h