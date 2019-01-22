from Module import MsSql
from Module import DataBase_Dict

def gongshi(date):
	conn_239 = DataBase_Dict['COMFROTSEATING']
	mssql = MsSql()
	sqlstr = (r"DELETE FROM CSTMB WHERE SUBSTRING(MB002,1,6)='{0}' "
	          r"INSERT INTO "
	          r"CSTMB(COMPANY,CREATOR,USR_GROUP,CREATE_DATE,MODIFIER,MODI_DATE,FLAG, "
	          r"MB001,MB002,MB003,MB004,MB005,MB006,MB007,MB008,MB009,MB010,MB011,MB012,MB013, "
	          r"UDF01,UDF02,UDF03,UDF04,UDF05,UDF06,UDF07,UDF08,UDF09,UDF10,UDF11,UDF12,UDF51,UDF52, "
	          r"UDF53,UDF54,UDF55,UDF56,UDF57,UDF58,UDF59,UDF60,UDF61,UDF62 ) "
	          r"select 'comfortwx','DS','','','','',1, "
	          r"MOCTA.TA021,CSTTA.TA002+'01',CSTTA.TA003,CSTTA.TA004,CSTTA.TA015,0,MOCTA.TA006,'','','',0,0,0, "
	          r"'','','','','','','','','','','','', "
	          r"0,0,0,0,0,0,0,0,0,0,0,0  "
	          r"from CSTTA CSTTA  "
	          r"INNER JOIN MOCTA MOCTA ON CSTTA.TA003=MOCTA.TA001 AND CSTTA.TA004=MOCTA.TA002  "
	          r"WHERE CSTTA.TA002='{0}' ")
	
	mssql.Sqlwork(DataBase=conn_239, SqlStr=sqlstr.format(date))
	print(sqlstr.format(date))
	return 'done'
