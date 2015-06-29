import ctypes, platform

name='Hello'
if platform.system()!='Windows': name='lib'+name+'.so'
hello=ctypes.CDLL(name)

def callback(text): print(text)
Callback=ctypes.CFUNCTYPE(None, ctypes.c_char_p)
hello.hello(Callback(callback))
