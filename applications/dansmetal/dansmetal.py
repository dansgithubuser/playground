import ast

class HardNodeVisitor(ast.NodeVisitor):
	def generic_visit(self, node):
		assert False, "unhandled node type: "+node.__class__.__name__

class C(HardNodeVisitor):
	#interface
	def result(self):
		r=''
		for header in self.headers: r+='#include <'+header+'.h>\n'
		r+='\n'+self.body
		return r

	#from HardNodeVisitor
	def visit(self, node):
		self.depth+=1
		HardNodeVisitor.visit(self, node)
		self.depth-=1

	def visit_Module(self, node):
		self.depth=0
		self.write_line('int main(){')
		ast.NodeVisitor.generic_visit(self, node)
		self.write_line('}')

	def visit_Print(self, node):
		self.include("stdio")
		format='"'
		for child in node.values:
			specifiers={
				'Str': 's'
			}
			format+='%'+specifiers[child.__class__.__name__]+' '
		format+=r'\n",'
		self.write_line('printf('+format)
		for child in node.values: self.visit(child)
		self.write_line(');')

	def visit_Str(self, node):
		self.write_line('"'+ast.literal_eval(node)+'"')

	#internal
	def __init__(self):
		self.headers=set()
		self.body=""
		self.depth=0

	def write_line(self, line):
		self.body+='\t'*self.depth+line+'\n'

	def include(self, library): self.headers.add(library)

def pro(meta, language):
	t=ast.parse(meta)
	l=language()
	l.visit(t)
	return l.result()

