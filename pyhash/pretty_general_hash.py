"""a pretty general kind-of-readable object hasher for comparing two different complex objects"""
def pretty_general_hash(x, indentation=0, inline=False, visited=None):
	#helpers
	def indent(indentation, s, inline=False):
		if inline:
			return s
		else:
			return '\t'*indentation+s
	def check_type(x, types):
		for t in types:
			if ("'"+t+"'") in str(type(x)):
				return True
		return False
	#visitations
	if visited==None: visited=[]
	if id(x) in visited: return indent(indentation, '\\reference\\', inline)
	visited.append(id(x))
	#recurse
	if hasattr(x, '__dict__'):
		d={}
		for k, v in x.__dict__.items():
			if not (k.startswith('__') and k.endswith('__')):
				d[k]=v
		return indent(
			indentation,
			str(type(x))+', __dict__:\n', inline)+pretty_general_hash(d, indentation+1,
			visited=visited
		)
	elif type(x) in [list, tuple, set]:
		result =indent(indentation, str(type(x))+'[\n', inline)
		result+=''.join([pretty_general_hash(
			e,
			indentation+1,
			visited=visited
		)+'\n' for e in x])
		result+=indent(indentation, ']')
		return result
	elif check_type(x, ['dict', 'dictproxy']):
		result =indent(indentation, '{\n', inline)
		result+=''.join([
			pretty_general_hash(k, indentation+1, visited=visited)
			+
			': '
			+
			pretty_general_hash(v, indentation+1, True, visited)
			+
			'\n'
			for k, v in x.items()
		])
		result+=indent(indentation, '}')
		return result
	elif type(x) in [bool, int, float, str, type(None)]:
		return indent(indentation, str(x), inline)
	elif check_type(x, ['weakref']):
		return pretty_general_hash(x(), indentation, inline, visited)
	else:
		return '\\unhandled type {0}\\'.format(type(x))
