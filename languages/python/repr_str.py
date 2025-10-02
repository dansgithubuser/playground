class C:
    def __repr__(self): return 'repr'
    def __str__(self): return 'str'

class D:
    def __repr__(self): return 'repr'

class E:
    def __str__(self): return 'str'

class F:
    pass

print('both       ', C())
print('repr only  ', D())
print('str only   ', E())
print('neither    ', F())
print()
print('inside a list')
print('both       ', [C()])
print('repr only  ', [D()])
print('str only   ', [E()])
print('neither    ', [F()])
