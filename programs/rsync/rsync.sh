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

rm -rf a b
