set -v

# filtering
# include stuff that ends in 2
# otherwise, exclude stuff that starts with x
# by default, include
./setup.sh
touch a/x1
touch a/x2
touch a/y1
touch a/y2
touch a/z1
touch a/z2
rsync -r --progress --filter='+ *2' --filter='- x*' a/ b
ls a
ls b

# filtering common use case, copy only one pattern
# include stuff that ends in 2
# otherwise, exclude
./setup.sh
touch a/x1
touch a/x2
touch a/y1
touch a/y2
touch a/z1
touch a/z2
rsync -r --progress --filter='+ *2' --filter='- *' a/ b
ls a
ls b

# gotcha: general excludes kill specific includes, regardless of filter order
# rsync traverses parents before children, and if we exclude a parent, we never evaluate children
# here the '- *' applies to I, so we never find I/i2
# even though the exclude filter is later
./setup.sh
mkdir a/I
touch a/I/i2
touch a/x2
rsync -r --progress --filter='+ *2' --filter='- *' a/ b
ls a
ls b

rm -rf a b
