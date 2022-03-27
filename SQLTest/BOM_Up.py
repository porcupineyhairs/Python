from SqlHelper import MsSqlHelper
import pandas as pd
import time

mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


def CpSelect(pinhao, pinhao2=None):
	if pinhao2 is None:
		pinhao2 = pinhao

	sqlStr = r"SELECT '{1}' 材料品号,RTRIM(MB025) 品号属性, RTRIM(MB001) 上阶, RTRIM(MB002) 品名, RTRIM(MB003) 规格  " \
			 r"FROM INVMB WHERE MB025='M' AND MB109='Y' AND MB001 = '{0}' "
	# print(sqlStr.format(pinhao2, pinhao))
	get = mssql.sqlWork(sqlStr=sqlStr.format(pinhao2, pinhao))

	if get is not None:
		rtnList.append(get[0])
		return rtnList
	else:
		return None


def Select(pinhao, pinhao2=None):
	global sqlCount
	if pinhao2 is None:
		pinhao2 = pinhao

	sqlStr = r"SELECT '{1}' 材料品号, RTRIM(MB025) 品号属性, RTRIM(CB001) 上阶, RTRIM(MB002) 品名, RTRIM(MB003) 规格 " \
		     r"FROM BOMCB INNER JOIN INVMB ON MB001 = CB001 AND MB109 = 'Y' " \
		     r"WHERE (ISNULL(RTRIM(CB014), '') = '' OR CB014 >= CONVERT(VARCHAR(8), GETDATE(), 112)) AND CB005 = '{0}' " \
			 r"ORDER BY CB001 "

	# print(sqlStr.format(pinhao2))

	get = mssql.sqlWork(sqlStr=sqlStr.format(pinhao2, pinhao))
	sqlCount += 1
	if get is not None:
		for row_tmp in get:
			shuxing = row_tmp[1]
			shangjie = row_tmp[2]

			if shuxing == 'M':
				rtnList.append(row_tmp)
				# print(row_tmp)
			else:
				Select(pinhao, shangjie)

	return rtnList


def getPh():
	df0 = pd.read_excel('000.xlsx')
	list2 = []
	for index in range(len(df0)):
		ph = str(df0.at[index, '主件品号'])
		list2.append(ph.rstrip())

	return list2


if __name__ == '__main__':
	# getPh()
	sqlCount = 1
	startdate = time.ctime()
	pinhao = ['24004481', '24000728', '24000695']
	# pinhao = getPh()
	rtnList = []
	for p_tmp in pinhao:
		if CpSelect(p_tmp) is None:
			r = Select(p_tmp)

	df = pd.DataFrame(columns=['材料品号', '品号属性', '成品品名', '成品品号', '成品规格'], data=rtnList)
	# 删除列
	df2 = df.drop(['材料品号', '品号属性'], axis=1)
	# # 去重
	df2.drop_duplicates(keep='first', inplace=True)
	df.to_excel('成品0.xlsx', sheet_name='Sheet1', index=False)

	enddate = time.ctime()
	print('开始时间:' + startdate)
	print('结束时间:' + enddate)
	# print(sqlCount)
	# print(len(rtnList))
