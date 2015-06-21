#include <stdio.h>

#ifdef _MSC_VER
	#define CTYPES __declspec(dllexport)
#else
	#define CTYPES
#endif

typedef void (*Callback)();

CTYPES void hello(Callback callback){ callback(); }
