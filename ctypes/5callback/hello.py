import ctypes, platform

name='Hello'
if platform.system()!='Windows': name='lib'+name+'.so'
hello=ctypes.CDLL(name)

def callback(): print("Hello!")

Callback=ctypes.CFUNCTYPE(None)

hello.hello(Callback(callback))
