# -*- coding: UTF-8 -*-
from SelfModule import MsSql
from LIB.ModuleDictionary import DataBase_Dict




if __name__ == '__main__':
	import pymssql
	conn = pymssql.connect(host='192.168.7.254', user='sa', password='comfort', database='COMFORT', charset='GBK')
	cur = conn.cursor()
	sql = r"INSERT INTO ZYH005 (ZN001, ZN002, ZN03) VALUES('222', '你好', 'N')"
	cur.execute(sql)
	conn.commit()
	conn.close()

