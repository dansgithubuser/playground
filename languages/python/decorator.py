def f(x, m=1):
    print('in decorator, x =', x, 'm =', m)
    x.m = m
    return x

print('declaring decorated class C')

@f
class C:
    pass

print('C.m =', C.m)

def g(m):
    return lambda x: f(x, m)

@g(2)
class D:
    pass

print('D.m =', D.m)
