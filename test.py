def aaaa():
	try:
		raise
	except:
		print("EXCEPTIONS!")
		raise

	print("hey")

try:
	aaaa()
except:
	print("PARENT:EX!")
