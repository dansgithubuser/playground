class Normal:
    def __new__(cls, *args, **kwargs):
        print('normal new')
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print(f'normal init {id(self)}')
        super().__init__(*args, **kwargs)

print('instantiate a Normal')
a = Normal()
print('instantiate a 2nd Normal')
b = Normal()

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        print('singleton new')
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        print(f'singleton init {id(self)}')
        if getattr(self, '_inited', False):
            return
        self._inited = True
        super().__init__(*args, **kwargs)
        print('singleton init inited')

print('')
print('instantiate a Singleton')
a = Singleton()
print('instantiate a 2nd Singleton')
b = Singleton()

class Subclass1(Singleton):
    pass

print('')
print('instantiate a Subclass1')
a = Subclass1()

class Subclass2(Singleton):
    _instance = None

print('')
print('instantiate a Subclass2')
a = Subclass2()
