import shutil, os, platform

shutil.rmtree('build', True)
os.makedirs('build')
os.chdir('build')
os.system('cmake -D BUILD_SHARED_LIBS=ON ..')
os.system('cmake --build .')
if platform.system()=='Linux':
	os.system('export LD_LIBRARY_PATH=`pwd`')
os.system('python ../hello.py')
