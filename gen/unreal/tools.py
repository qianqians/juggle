# 2016-7-1
# build by qianqians
# tools

def gentypetocpp(typestr):
    if typestr == 'int':
        return 'int64'
    elif typestr == 'string':
        return 'FString'
    elif typestr == 'array':
        return 'TArray< TSharedPtr<FJsonValue> >*'
    elif typestr == 'float':
        return 'double'
    elif typestr == 'bool':
        return 'bool'
    elif typestr == 'table':
        return 'TSharedPtr<FJsonObject>*'

def gengetargvfromunreal(typestr):
	if typestr == 'int':
        return 'TryGetNumber'
    elif typestr == 'string':
        return 'TryGetString'
    elif typestr == 'array':
        return 'TryGetArray'
    elif typestr == 'float':
        return 'TryGetNumber'
    elif typestr == 'bool':
        return 'TryGetBool'
    elif typestr == 'table':
        return 'TryGetObject'

def genjsonvaluetypefromunreal(typestr):
	if typestr == 'int':
        return 'FJsonValueNumber'
    elif typestr == 'string':
        return 'FJsonValueString'
    elif typestr == 'array':
        return 'FJsonValueArray'
    elif typestr == 'float':
        return 'FJsonValueNumber'
    elif typestr == 'bool':
        return 'FJsonValueBoolean'
    elif typestr == 'table':
        return 'FJsonValueObject'