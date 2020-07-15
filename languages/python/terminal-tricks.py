print('1234567890', end='\r')
print('abc')

for i in range(10):
    print('\t'*8 + '|')

for i in range(8):
    print('\033[F', end='')

for i in 'abcdef':
    print(i)
