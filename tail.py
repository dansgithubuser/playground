import sys, time
with open(sys.argv[1]) as file:
	while True:
		sys.stdout.write(file.read())
		time.sleep(0.1)
