import ctypes

l=ctypes.CDLL('libClass.so')

l.consumeClass(l.createClass())
