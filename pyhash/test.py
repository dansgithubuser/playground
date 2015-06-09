from pretty_general_hash import pretty_general_hash as f

def section(): print('='*72)

section()
print(f(1))
print(None)
print(1.0)
print('str')

section()
print(f(dir(dir)))

section()
print(f(section))

section()
class C:
	def __init__(self): self.x=3

print(f(C))

section()
print(f(C()))

section()
def random_thing(x):
	period=10
	if x%period==0: return random_list(x-1)
	if x%period==1: return random_dict(x-1)
	if x%period==2: return random_tuple(x-1)
	if x%period==3: return random_set(x-1)
	return x

def random_list(x): return [random_thing(i) for i in range(x/2)]

def random_dict(x):
	result={}
	for i in range(x/2):
		result[i]=random_thing(i)
	return result

def random_tuple(x): return tuple(random_list(x))

def random_set(x): return set([i for i in range(x%4+2)])

x=random_list(25)
print(x)
print(f(x))

section()
x=[0, 1]
y=[0, 2]
x[0]=y
y[0]=x
print(f(x))
