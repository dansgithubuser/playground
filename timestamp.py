def timestamp():
	import datetime
	return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

if __name__=='__main__': print(timestamp())

