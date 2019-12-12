import cx_Oracle

oracleConn = cx_Oracle.Connection("test/test@10.10.10.50:1521/orcl")
c = oracleConn.cursor()
error = ''
try:
	kk = c.execute(" select 1 / 0 from dual ")
	print(str(kk))
	print(c.description)
except Exception as e:
	error = str(e)
	print(error)
	print(type(error))
	print("Oracle-Error-Code:", str(error).split(':')[0].strip())
	print("Oracle-Error-Message:", str(error).split(':')[1].strip())
