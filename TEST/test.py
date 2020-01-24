
def test0(index=0):
	ret = 0
	if index > 0:
		ret = 0.01
		for index_tmp in range(1, index, 1):
			ret += ret*2
	else:
		pass

	return ret

kk = test0(30)
print(kk)