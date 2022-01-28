from modules.SqlHelper import MsSqlHelper
import datetime


class CreateMoctg:
	def __init__(self):
		self.mssql = MsSqlHelper(host='comfort-oa.com:60043', database='COMFORT', user='sa', passwd='comfortgroup2016{')
		
	def get(self):
		sql_str = r"SELECT TG001 销货单别, TG002 销货单号, TH001 销货序号, " \
		          r"RTRIM(TH004) 品号, RTRIM(TH005) 品名, RTRIM(TH006) 规格, " \
		          r"CAST(TH008 AS FLOAT) 销货数量 " \
		          r"FROM COPTG " \
		          r"INNER JOIN COPTH ON TG001 = TH001 AND TG002 = TH002 " \
		          r"WHERE RTRIM(TG001)+'-'+RTRIM(TG002) = '2301-21090001' " \
		          r"ORDER BY TH003"
		data_info = self.mssql.sqlWork(sql_str)
		return data_info.to_json()
