from Module import Sql
from Module import DataBase_Dict

connStr = DataBase_Dict['Ls']
sql = Sql(connDict=DataBase_Dict['Ls'], sqlType='mssql')


sqlstr_scd = r"select top 2 scdh, wlno, sl, bz, scrq, scjq from mf_wwd where shbz = 1order by scjq"

sqlstr_wlno = r"select scd_no, wlno, name, spec, wllx from tf_scd where scd_no = '{0}' order by seq"

sqlstr_bom = r"select * from tf_bom where bom_no = '{0}' order by seq"


get_scd = sql.SqlWork(sqlStr=sqlstr_scd, getRowCount=False)
print(get_scd)






