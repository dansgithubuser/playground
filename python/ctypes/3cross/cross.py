import ctypes

a=ctypes.CDLL('libA.so')
b=ctypes.CDLL('libB.so')

b.consumeClass(a.createClass())
