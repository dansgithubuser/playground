import os

for root, dirs, files in os.walk('.'):
    print('root:', root)
    print('dirs:', dirs)
    print('files:', files)
    print()
