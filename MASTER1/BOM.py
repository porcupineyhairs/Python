from SelfModule import MsSql
import time
import sqlite3
import LIB.ModuleDictionary

mssql = MsSql()


def WriteFile(Name='', List=[]):
	f = open(str(Name) + ".txt", 'a+')
	f.writelines(List)
	f.close()


def SelectSqlite3(sqlcmd):
	GetBack = []
	conn = sqlite3.connect("./DB.db")
	cur = conn.cursor()
	cur.execute(sqlcmd)
	conn.commit()
	res = cur.fetchall()
	# 关闭连接
	cur.close()
	conn.close()
	if len(res) == 0:
		GetBack = None
	for List in res:
		GetBack.append(list(List))
	return GetBack


def Select(pinhao, level=0):
	if level == 0:
		global count
		count += 1
		Str0 = 'SELECT RTRIM(MB002), RTRIM(MB003), RTRIM(MB025) FROM INVMB WHERE MB001 = \'' + str(pinhao) + '\''
		get = mssql.Sqlwork(DataBase=LIB.ModuleDictionary.DataBase_Dict.get('COMFORT'), SqlStr=Str0, GetRowCount=False)
		print(str(level) + '|-' + '\t' + pinhao + '\t' + get[0][0] + '\t' + get[0][1] + '\t' + get[0][2])
		STR.append(str(level) + '|-' + '\t' + pinhao + '\t' + get[0][0] + '\t' + get[0][1] + '\t' + get[0][2] + '\n')
		level += 1

	Str0 = (r"SELECT DISTINCT "
			r"RTRIM(CB005), "  # 本阶品好
			r"RTRIM(MB002), "  # 品名
			r"RTRIM(MB003), "  # 规格
			r"RTRIM(CB004), "  # 序号
			r"RTRIM(INVMB.MB025), "  # 品号属性
			# r"RTRIM(INVMB.MB109), "  # 核准状况
			r"RTRIM(MW001), "  # 工艺编码
			# r"RTRIM(MW002), "     # 工艺名称
			r"(CASE WHEN RTRIM(CB013) IS NULL THEN '' WHEN RTRIM(CB013) = '' THEN '' "
			r"ELSE SUBSTRING(RTRIM(CB013),1,4) + '-' + SUBSTRING(RTRIM(CB013),5,2) + '-' +SUBSTRING(RTRIM(CB013),7,2) END ), "
			r"(CASE WHEN RTRIM(CB014) IS NULL THEN '' WHEN RTRIM(CB014) = '' THEN '' "
			r"ELSE SUBSTRING(RTRIM(CB014),1,4) + '-' + SUBSTRING(RTRIM(CB014),5,2) + '-' +SUBSTRING(RTRIM(CB014),7,2) END ), "
			r"RTRIM(PURMA.MA002) "  # 供应商名称
			# r"RTRIM(INVMA.MA003) "        # 会计类别
			r"FROM BOMCB  "
			r"LEFT JOIN CMSMW ON MW001 = CB011 "
			r"LEFT JOIN INVMB ON CB005 = INVMB.MB001 "
			r"LEFT JOIN BOMCA ON CA003 = CB005 "
			r"LEFT JOIN INVMA ON INVMA.MA002 = INVMB.MB005 "
			r"LEFT JOIN PURMA ON PURMA.MA001 = INVMB.MB032 "
			r"WHERE CB001 = '" + str(pinhao) + r"' "  # 上阶品号
			r"ORDER BY RTRIM(CB004) ")

	get = mssql.Sqlwork(DataBase=LIB.ModuleDictionary.DataBase_Dict.get('COMFORT'), SqlStr=Str0, GetRowCount=False)
	if get[0] != 'None':
		for row in range(len(get)):
			count += 1
			pinhao2 = get[row][0]
			pinming = get[row][1]
			guige = get[row][2]
			xuhao = get[row][3]
			shuxing = get[row][4]
			# hezhun = get[row][5]
			gongyi = get[row][6]
			shengxiao = get[row][7]
			shixiao = get[row][8]
			# gongyinshang = get[row][9]
			# kuaiji = get[row][10]

			# if gongyinshang not in ['保友', '玖友公司', '耀友五金']:
			# 	gongyinshang = '其他供应商'

			shuxingLib = {'P': '采购件', 'S': '委外件', 'C': '配置件', 'Y': '虚设件', 'M': '自制件'}
			shuxing2 = shuxingLib[str(shuxing)]

			PrintStr = ('\t' * int(level) + str(level) + '|-' + '\t' + pinhao2 + '\t' + pinming + '\t' + guige + '\t'
						+ xuhao + '\t' + shuxing2 + '\t' + gongyi )

			STR.append(PrintStr + '\n')
			print(PrintStr)

			if shuxing != 'P':
				Select(pinhao2, level + 1)

	return STR


if __name__ == '__main__':
	startdate = time.ctime()
	pinhao = ['10570530']
	# pinhao = ['10860105', '10860108', '10910105', '10910107', '10910109']
	for p in pinhao:
		STR = []
		count = 0
		r = Select(p)
		WriteFile(p, STR)

		print('共有' + str(count) + '项!\n\n\n')
	enddate = time.ctime()
	print('开始时间:' + startdate)
	print('结束时间:' + enddate)
	print(len(STR))
