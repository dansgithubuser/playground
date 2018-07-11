def f():
	try:
		raise Exception('lol')
	except Exception as e:
		e.rofl='100%'
		raise

try: f()
except Exception as e:
	print(e)
	print(e.rofl)
