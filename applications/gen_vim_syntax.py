import os
import shutil

form='''\
syn match n{0} /{0}/
highlight n{0} ctermfg={1}
'''

with open('rainbow_numbers.vim', 'w') as file:
	for i in range(100):
		n='{:02}'.format(i)
		file.write(form.format(n, i+1))

shutil.copyfile('rainbow_numbers.vim',
	os.path.join(os.path.expanduser('~'),
		'.vim', 'syntax', 'rainbow_numbers.vim'))
