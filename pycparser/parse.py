import pycparser

use_cpp=False
cpp_path='cmd'
cpp_args=''

ast=pycparser.parse_file('say.h', use_cpp=use_cpp, cpp_path=cpp_path, cpp_args=cpp_args)
ast.show()

