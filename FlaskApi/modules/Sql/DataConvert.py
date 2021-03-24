
def list2dict(getList):
	getBack = []
	if getList is not None:
		title = getList.pop(0)

		for row in getList:
			getBackTmp = {}
			for index in range(len(title)):
				getBackTmp.update({title[index]: row[index]})
			getBack.append(getBackTmp)
	return getBack
