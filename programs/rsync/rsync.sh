set -v

# a into b
./setup.sh
rsync -r --progress a b
ls a
ls b

# contents of a into b
./setup.sh
rsync -r --progress a/ b
ls a
ls b

# also contents of a into b
./setup.sh
rsync -r --progress a// b
ls a
ls b

# ALSO contents of a into b, surprise!
./setup.sh
cd a
rsync -r --progress . ../b
cd ..
ls a
ls b

# rsync without -t is scp -r
./setup.sh
sleep 2 # make sure files in b are created at different time than files in a
rsync -r --progress a/ b
rsync -r --progress a/ b
# surprise! all copied again
ls a
ls b

# rsync with -t does what you want
./setup.sh
sleep 2 # make sure files in b are created at different time than files in a
rsync -t -r --progress a/ b
rsync -t -r --progress a/ b
# that worked correctly
ls a
ls b

rm -rf a b
