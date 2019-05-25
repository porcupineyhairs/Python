def __numToChar(init_number):
	increment = ord('A') - 1
	char = chr(init_number + increment)
	if char == '@':
		return 'Z'
	else:
		return char


def changeNumToChar(toBigChar=None):
	char = ''
	if not toBigChar:
		return None
	else:
		shang, yu = divmod(toBigChar, 26)
		if shang == 1 and yu == 0:
			char += __numToChar(26)

		elif shang:
			char += changeNumToChar(shang)
			char += __numToChar(yu)
		else:
			char = __numToChar(yu)
		return char
