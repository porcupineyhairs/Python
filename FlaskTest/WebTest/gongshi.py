from Module import MsSql
from Module import DataBase_Dict


def test():
	conn_239 = DataBase_Dict['COMFROTSEATING']
	mssql = MsSql()
	sqlstr = r"SELECT MA011 FROM CMSMA "
	get = mssql.Sqlwork(DataBase=conn_239, SqlStr=sqlstr)
	print(get)
	return get[0][0]
