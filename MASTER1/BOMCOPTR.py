from SelfModule import MsSql
import time
import sqlite3
import LIB.ModuleDictionary

mssql = MsSql()
Conn_ERP = LIB.ModuleDictionary.DataBase_Dict.get('COMFORT')


def Main():
	startdate = time.ctime()
	pinhao = ['10710101']
	for p in pinhao:
		STR = []
		r = Select(pinhao=p, List=STR)

		print('共有' + str(len(STR)) + '项!\n\n\n')
	enddate = time.ctime()
	print('开始时间:' + startdate)
	print('结束时间:' + enddate)


def GetToday():
	__SqlStr = r"SELECT CONVERT(VARCHAR(20), GETDATE(), 112)"
	__Today = mssql.Sqlwork(DataBase=Conn_ERP, SqlStr=__SqlStr)
	if len(__Today) > 0:
		__Today = __Today[0][0]
		return __Today
	else:
		return None


def Select(pinhao, level=0, List=None, LevelList=None):
	__Today = GetToday()

	if LevelList is None:
		LevelList = [pinhao]

	if level == 0:
		Str0 = 'SELECT RTRIM(MB002), RTRIM(MB003), RTRIM(MB025) FROM INVMB WHERE MB001 = \'' + str(pinhao) + '\''

		get = mssql.Sqlwork(DataBase=Conn_ERP, SqlStr=Str0)

		print(str(level) + '|-' + '\t' + pinhao + '\t' + get[0][0] + '\t' + get[0][1] + '\t' + get[0][2])
		List.append(str(level) + '|-' + '\t' + pinhao + '\t' + get[0][0] + '\t' + get[0][1] + '\t' + get[0][2] + '\n')
		level += 1

	Str0 = (r"SELECT DISTINCT "
			r"RTRIM(CB005), "  # 本阶品好
			r"RTRIM(MB002), "  # 品名
			r"RTRIM(MB003), "  # 规格
			r"RTRIM(CB004), "  # 序号
			r"RTRIM(INVMB.MB025), "  # 品号属性
			r"RTRIM(INVMB.MB109), "  # 核准状况
			r"RTRIM(MW001), "  # 工艺编码
			r"RTRIM(CB013), "
			r"RTRIM(CB014) "
			r"FROM BOMCB  "
			r"LEFT JOIN CMSMW ON MW001 = CB011 "
			r"LEFT JOIN INVMB ON CB005 = INVMB.MB001 "
			r"LEFT JOIN BOMCA ON CA003 = CB005 "
			r"LEFT JOIN INVMA ON INVMA.MA002 = INVMB.MB005 "
			r"LEFT JOIN PURMA ON PURMA.MA001 = INVMB.MB032 "
			r"WHERE CB001 = '" + str(pinhao) + r"' "  # 上阶品号
			r"AND (CB014 IS NULL OR CB014 = '' OR CB014 > '" + __Today + r"') "
			r"AND MB109 = 'Y' "
			r"ORDER BY RTRIM(CB004) ")

	get = mssql.Sqlwork(DataBase=Conn_ERP, SqlStr=Str0)

	if get[0] != 'None':
		for row in range(len(get)):
			pinhao2 = get[row][0]
			pinming = get[row][1]
			guige = get[row][2]
			xuhao = get[row][3]
			shuxing = get[row][4]
			hezhun = get[row][5]
			gongyi = get[row][6]
			shengxiao = get[row][7]
			shixiao = get[row][8]

			if shuxing == 'C':
				print(pinhao2)
				LevelList3 = LevelList[:]
				LevelList3.append(str(pinhao2) + str(xuhao) + str(gongyi) + str(shengxiao))
				print(str(level) + '    ' + str(LevelList3))

			if shuxing == 'P':
				PrintStr = ('\t' * int(level) + str(level) + '|-' + '\t' + pinhao2 + '\t' + pinming + '\t' + str(
					guige) + '\t' + xuhao + '\t' + shuxing + '\t' + gongyi + '\t' + shengxiao + '\t' + shixiao)

				List.append(PrintStr + '\n')

			if shuxing != 'P':
				LevelList2 = LevelList[:]
				LevelList2.append(str(pinhao2) + str(xuhao) + str(gongyi) + str(shengxiao))
				# print(LevelList2)
				Select(pinhao=pinhao2, level=level + 1, List=List, LevelList=LevelList2)

	# PrintStr = ('\t' * int(level) + str(level) + '|-' + '\t' + pinhao2 + '\t' + pinming + '\t' + str(guige) + '\t'
	# 			+ xuhao + '\t' + shuxing + '\t' + gongyi + '\t' + shengxiao + '\t' + shixiao)
	#
	# List.append(PrintStr + '\n')
	#
	# print(PrintStr)

	return List


if __name__ == '__main__':
	Main()
