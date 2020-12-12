from MsSql import MsSqlHelper

mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


def main():
	sqlStr1 = r"SELECT RTRIM(TA001), RTRIM(TA002) FROM MOCTA WHERE TA001 = '5101' AND TAU01 IS NULL ORDER BY TA001, TA002"
	
	sqlStr2 = r"UPDATE MOCTA SET TAU01 = RTRIM(MB001), TAU02 = MBU01 " \
	          r"FROM MOCTA " \
	          r"INNER JOIN (" \
	          r"	SELECT TOP 1 TB001, TB002, MB001, MB003, MBU01, MBU02 " \
	          r"	FROM MOCTB " \
	          r"	INNER JOIN INVMB ON MB001 = TB003 AND (MB002 LIKE '%纸箱%' OR MB002 LIKE '%彩盒%' OR MB002 LIKE '%天地盖%')" \
	          r"	WHERE 1=1 " \
	          r"	AND TB004 > 0 " \
	          r"	AND TB011 != '4'" \
	          r"	AND TB001 = '{TA001}' " \
	          r"	AND TB002 = '{TA002}' " \
	          r"	ORDER BY MBU02 DESC " \
	          r") AS MOCTB ON TB001 = TA001 AND TB002 = TA002 " \
	          r"WHERE (TAU01 IS NULL OR TAU01 != RTRIM(MB001))"
	
	get = mssql.sqlWork(sqlStr1)
	
	if get is not None:
		for tmp in get:
			print(tmp)
			mssql.sqlWork(sqlStr2.format(TA001=tmp[0], TA002=tmp[1]))


if __name__ == '__main__':
	main()
	