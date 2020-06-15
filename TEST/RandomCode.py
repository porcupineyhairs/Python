#coding:utf-8
import random
import string
import csv

def GetPassword(length):
	# 随机生成数字个数
	Ofnum=random.randint(1,length - 3)
	Ofletter=length-Ofnum
	# 选中ofnum个数字
	slcNum=[random.choice(string.digits) for i in range(Ofnum)]
	# 选中ofletter个字母
	slcLetter=[random.choice(string.ascii_letters) for i in range(Ofletter)]
	# 打乱组合
	slcChar=slcLetter+slcNum
	random.shuffle(slcChar)
	# 生成随机密码
	getPwd=''.join([i for i in slcChar])
	getPwd = getPwd.lower()
	return getPwd


def CheckGet(get):
	try:
		kk = int(get)
		get = GetPassword(8)
		print('old:' + str(kk) + '  new:' + get)
	except:
		pass
	return get


def Generate(count):
	passWdLenth = 8
	listTmp = []
	for i in range(0, count):
		get = GetPassword(passWdLenth)
		listTmp.append(get)
	return  listTmp


def SaveCsv(saveList):
	with open('password.xlxs', 'w')as f:
		f_csv = csv.writer(f)
		f_csv.writerows(saveList)


if __name__=='__main__':
	# print( GetPassword(8)) #GetPassword()自定义随机密码长度
	colCount = 20
	rowCount = 121
	listTmp = Generate(rowCount * colCount)

	saveList = []
	listTmp2 = []
	listTmpLen = len(listTmp)

	for i in range(0, listTmpLen):
		listTmp[0] = CheckGet(listTmp[0])

		listTmp2.append(listTmp.pop(0))
		if len(listTmp2) == colCount:
			saveList.append(listTmp2)
			listTmp2 = []

	# for kk in saveList:
	# 	print(kk)
	SaveCsv(saveList)