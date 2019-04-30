rm -rf build
mkdir build
cd build
cmake -D BUILD_SHARED_LIBS=ON ..
make
export LD_LIBRARY_PATH=`pwd`
cd ..
python inherit.py
