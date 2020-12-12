
from MsSql import MsSqlHelper


mssqlYF = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')
mssqlWG = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='WG_DB')


def main():
	sqlstr = "SELECT ROW_NUMBER() OVER(ORDER BY SC003, SC001, SC023, SC013, CREATE_DATE) AS XH, " \
	         "K_ID, SC003, SC001, SC013, SC023, CREATE_DATE FROM SC_PLAN ORDER BY SC003, SC001, SC023, SC013, CREATE_DATE "
	
	sqlStr2 = "UPDATE SC_PLAN SET K_ID = '{5}' WHERE K_ID = '{0}' AND SC003 = '{1}' AND SC001 = '{2}' AND SC023 = '{3}' " \
	          "AND CREATE_DATE = '{4}'"

	get = mssqlWG.sqlWork(sqlstr)
	
	if get is not None:
		for tmp in get:
			xh = tmp[0]
			kid = tmp[1]
			sc003 = tmp[2]
			sc001 = tmp[3]
			sc023 = tmp[5]
			sc013 = tmp[4]
			cd = tmp[6]
			print(tmp)
			# print(sqlStr2.format(kid, sc003, sc001, sc023, cd, xh))
			mssqlWG.sqlWork(sqlStr2.format(kid, sc003, sc001, sc023, cd, xh))


if __name__ == '__main__':
	main()