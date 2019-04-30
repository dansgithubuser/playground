import ctypes

derived=ctypes.CDLL('libDerived.so')
polymorph=ctypes.CDLL('libPolymorph.so')

family=[]
for i in range(5):
    if i%2:
        x=derived.create()
    else:
        x=polymorph.create()
    family.append(x)

for member in family: polymorph.consume(member)
