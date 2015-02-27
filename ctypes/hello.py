import ctypes

hello=ctypes.CDLL('libHello.so')

hello.hello()
