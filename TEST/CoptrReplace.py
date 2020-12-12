# 用于替换易飞客户配置中的勾选项
# 会修改COPTR表，慎用
# 只需要修改映射关系和主Sql语句即可

from MsSql import MsSqlHelper

# 被替换品号和新品号的映射关系
ph_list = [['3010305017', '3010305021'],
           ['3010305018', '3010305023'],
           ['3010305019', '3010305022'],
           ['3010305020', '3010305024']]

# 主Sql语句，确定客户配置的范围
mainSqlStr = r"SELECT DISTINCT RTRIM(TQ001), RTRIM(TQ002)  " \
	         r"FROM COPTQ(NOLOCK) " \
	         r"LEFT JOIN COPTR(NOLOCK) ON TQ001=TR001 AND TQ002=TR002 " \
	         r"WHERE TR009 IN ('3010305017', '3010305018', '3010305019', '3010305020') " \
	         r"AND TR017 = 'Y' " \
	         r"AND TQ006 = 'Y' " \
	         r"ORDER BY RTRIM(TQ001), RTRIM(TQ002) "


mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


def work(tmp_list):
	tr1 = tmp_list[0]
	tr2 = tmp_list[1]
	print('1. ' + tr1 + '-' + tr2)
	for ph_tmp in ph_list:
		ph1 = ph_tmp[0]
		ph2 = ph_tmp[1]
		getTr3 = existTr3(tr1, tr2, ph1)
		if getTr3 is not None:
			print('2. ' + 'PH1:' + ph1 + '     TR3:' + str(getTr3))
			for tr3_tmp in getTr3:
				tr3 = tr3_tmp[0]
				print('3. ' + tr3)
				if existPh(tr1, tr2, tr3, ph2):
					print('4. ' + tr1, tr2, tr3)
					replacePh(tr1, tr2, tr3, ph1, ph2)
				else:
					print('5. not exist ph2')



def existTr3(tr1, tr2, ph):
	sqlStr = r"SELECT SUBSTRING(TR003, 1, LEN(TR003)-3) FROM COPTR WHERE TR001='{0}' AND TR002='{1}' AND TR009='{2}' " \
	         r"AND TR017='Y'"
	# print('existTr3: ' + sqlStr.format(tr1, tr2, ph))
	get = mssql.sqlWork(sqlStr.format(tr1, tr2, ph))
	return get


def existPh(tr1, tr2, tr3, ph):
	sqlStr = r"SELECT TR017 FROM COPTR WHERE TR001='{0}' AND TR002='{1}' AND SUBSTRING(TR003, 1, LEN(TR003)-3)='{2}' " \
	         r"AND TR009='{3}' AND TR017 = 'N' "
	# print('existPh: ' + sqlStr.format(tr1, tr2, tr3, ph))
	get = mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph))
	return True if get is not None else False


def replacePh(tr1, tr2, tr3, ph1, ph2):
	sqlStr = r"UPDATE COPTR SET TR017='{4}' " \
	         r"WHERE TR001='{0}' AND TR002='{1}' AND SUBSTRING(TR003, 1, LEN(TR003)-3)='{2}' AND TR009='{3}' "
	print('replacePh: ' + sqlStr.format(tr1, tr2, tr3, ph2, 'Y'))
	mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph2, 'Y'))
	print('replacePh: ' + sqlStr.format(tr1, tr2, tr3, ph1, 'N'))
	mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph1, 'N'))


def main():
	mainGet = mssql.sqlWork(sqlStr=mainSqlStr)
	if mainGet is not None:
		for tmp in mainGet:
			work(tmp)
			print()
			print()


if __name__ == '__main__':
	main()