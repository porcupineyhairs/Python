def list2Dict(_list):
	# if type(_list) == r"<class 'list'>":
	if True:
		rtnList = []
		for rowIdx in range(1, len(_list)):
			dictTmp = {}
			for colIdx in range(len(_list[0])):
				dictTmp.update({_list[0][colIdx]: _list[rowIdx][colIdx]})
			rtnList.append(dictTmp)
		return rtnList
	else:
		return None
