import os, sys
for line in sys.stdin:
	for file in line.split():
		os.system(sys.argv[1].format(file))
