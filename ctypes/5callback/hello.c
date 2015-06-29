#include <stdio.h>

#ifdef _MSC_VER
	#define CTYPES __declspec(dllexport)
#else
	#define CTYPES
#endif

typedef void (*Callback)(char*);

CTYPES void hello(Callback callback){ callback("Hello, world!"); }
