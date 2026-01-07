def print_on_call(f):
    print('in print_on_call')
    def g(*args, **kwargs):
        print('in print_on_call inner function')
        f(*args, **kwargs)
    return g

print('\ndecorating function')
@print_on_call
def f(*args, **kwargs):
    print(f'in f {args=} {kwargs=}')

print('\ncalling decorated function')
f()

print('\ndecorating class')
@print_on_call
class C:
    def __init__(self):
        print('in C.__init__')

print('\ninstantiating decorated class')
C()

def outer_decorator(f):
    print('in outer_decorator')
    f = print_on_call(f)
    def g(*args, **kwargs):
        print('in outer_decorator inner function')
        f(*args, **kwargs)
    return g

print('\nouter-decorating function')
@outer_decorator
def f(*args, **kwargs):
    print(f'in f {args=} {kwargs=}')

print('\ncalling outer-decorated function')
f(1, 2, z=3)

def decorator(f=None, a=None):
    print(f'{f=} {a=}')
    return lambda f: print(f'{f=}')

print('\nusing decorator without params')
@decorator
def f(): pass

print('\nusing decorator with param')
@decorator(a=1)
def f(): pass
