from Module import Sql
import time
import sqlite3

sql = Sql(sqlType='mysql', connDict=['127.0.0.1', 'root', 'Tiamohui', 'COMFORT', 'utf8'])
# sql = Sql(sqlType='mssql', connDict=['192.168.0.99', 'sa', 'comfortgroup2016{', 'COMFORT', 'GBK'])


def WriteFile(Name='', List=[]):
	f = open(str(Name) + ".txt", 'a+')
	f.writelines(List)
	f.close()


def Select(pinhao, level=0):
	if level == 0:
		global count
		count += 1
		Str0 = r"SELECT RTRIM(MB002), RTRIM(MB003), RTRIM(MB025) FROM INVMB WHERE MB001 = '{0}' "
		get = sql.SqlWork(sqlStr=Str0.format(pinhao))
		print(str(level) + '|-' + '\t' + pinhao + '\t' + get[0][0] + '\t' + get[0][1] + '\t' + get[0][2])
		STR.append(str(level) + '|-' + '\t' + pinhao + '\t' + get[0][0] + '\t' + get[0][1] + '\t' + get[0][2] + '\n')
		level += 1

	Str0 = (r"SELECT DISTINCT "
	        r"RTRIM(CB005), "  # 本阶品好
	        r"RTRIM(MB002), "  # 品名
	        r"RTRIM(MB003), "  # 规格
	        r"RTRIM(CB004), "  # 序号
	        r"(CASE RTRIM(INVMB.MB025) WHEN 'P' THEN '采购件' WHEN 'S' THEN '委外件' WHEN 'C' THEN '配置件' "
	        r"WHEN 'Y' THEN '虚设件' WHEN 'M' THEN '自制件' ELSE RTRIM(INVMB.MB025) END),"  # 品号属性
	        # r"RTRIM(INVMB.MB109), "  # 核准状况
	        r"RTRIM(MW001), "  # 工艺编码
	        # r"RTRIM(MW002), "     # 工艺名称
	        r"(CASE WHEN RTRIM(CB013) IS NULL THEN '' WHEN RTRIM(CB013) = '' THEN '' "
	        r"ELSE CONCAT(SUBSTRING(RTRIM(CB013),1,4), '-', SUBSTRING(RTRIM(CB013),5,2), '-', "
	        r"SUBSTRING(RTRIM(CB013),7,2)) END ), "
	        r"(CASE WHEN RTRIM(CB014) IS NULL THEN '' WHEN RTRIM(CB014) = '' THEN '' "
	        r"ELSE CONCAT(SUBSTRING(RTRIM(CB014),1,4), '-', SUBSTRING(RTRIM(CB014),5,2), '-', "
	        r"SUBSTRING(RTRIM(CB014),7,2)) END ), "
	        r"RTRIM(PURMA.MA002), RTRIM(CB015) "  # 供应商名称
	        # r"RTRIM(INVMA.MA003) "# 会计类别
	        r"FROM BOMCB  "
	        r"LEFT JOIN CMSMW ON MW001 = CB011 "
	        r"LEFT JOIN INVMB ON CB005 = INVMB.MB001 "
	        r"LEFT JOIN BOMCA ON CA003 = CB005 "
	        r"LEFT JOIN INVMA ON INVMA.MA002 = INVMB.MB005 "
	        r"LEFT JOIN PURMA ON PURMA.MA001 = INVMB.MB032 "
	        r"WHERE CB001 = '{0}' "  # 上阶品号
	        r"ORDER BY RTRIM(CB004) ")

	get = sql.SqlWork(sqlStr=Str0.format(pinhao))
	if get is not None:
		for row in range(len(get)):
			count += 1
			pinhao2 = get[row][0]
			pinming = get[row][1]
			guige = get[row][2]
			xuhao = get[row][3]
			shuxing = get[row][4]
			gongyi = get[row][5]
			shengxiao = get[row][6]
			shixiao = get[row][7]
			moren = get[row][9]

			PrintStr = ('\t' * int(level) + str(level) + '|-' + '\t' + pinhao2 + '\t' + pinming + '\t' + guige + '\t' +
			            xuhao + '\t' + shuxing + '\t' + gongyi + '\t' + shengxiao + '\t' + shixiao + '\t' + moren)

			STR.append(PrintStr + '\n')
			print(PrintStr)

			if shuxing != '采购件2':
				Select(pinhao2, level + 1)

	return STR


if __name__ == '__main__':
	startdate = time.ctime()
	pinhao = ['10710101']
	for p in pinhao:
		STR = []
		count = 0
		r = Select(p)
		# WriteFile(p, STR)

		print('共有' + str(count) + '项!\n\n\n')
	enddate = time.ctime()
	print('开始时间:' + startdate)
	print('结束时间:' + enddate)
