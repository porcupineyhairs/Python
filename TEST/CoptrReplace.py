from MsSql import MsSqlHelper
ph_list = [['3010301014', '3010301023'], ['3010301015', '3010301024'], ['3010301016', '3010301025'],
           ['3010301017', '3010301026'], ['3010301018', '3010301027'], ['3010301019', '3010301028'],
           ['3010301020', '3010301029'], ['3010301021', '3010301030'], ['3010301022', '3010301031']]

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
	# mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph2, 'Y'))
	print('replacePh: ' + sqlStr.format(tr1, tr2, tr3, ph1, 'N'))
	# mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph1, 'N'))


def main():
	sqlStr = r"SELECT RTRIM(TQ001), RTRIM(TQ002) FROM COPTQ WHERE TQ002 LIKE '%ZB%' AND TQ002 LIKE '%保友%'  " \
	         r"AND TQ006 = 'Y' " \
	         r"ORDER BY TQ001, TQ002"

	mainGet = mssql.sqlWork(sqlStr=sqlStr)
	if mainGet is not None:
		for tmp in mainGet:
			work(tmp)
			print()
			print()


if __name__ == '__main__':
	main()