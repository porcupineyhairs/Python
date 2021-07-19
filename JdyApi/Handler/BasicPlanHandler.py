from JdyHelper.JdyApi import APIUtils
from BaseHelper import MsSqlHelper
import datetime
import pandas as pd


# 生产排程表
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
entryId = '60d15f664e8ede0007264a08'

api = APIUtils(appId, entryId, api_key)
mssql = MsSqlHelper(host='comfort-oa.com:60043', user='sa', passwd='comfortgroup2016{', database='WG_DB')


def main_work():
	print('生产排程表')
	create_plan()


def create_plan():
	sqlStr_getPlan = r"SELECT top 2 K_ID plan_index, SC001 order_id, SC002 order_type, " \
	                 r"SC003 plan_date, SC004 custmer_name, SC013 plan_num, SC023 plan_dept, " \
	                 r"MB001 wlno, MB002 wlno_name, MB003 wlno_spec, INVMB.UDF01 wlno_series " \
	                 r"FROM SC_PLAN " \
	                 r"INNER JOIN COMFORT.dbo.INVMB ON MB001 = SC028 " \
	                 r"WHERE JdyId is null " \
	                 r"order by SC003, SC001 "

	sqlStr_setPlan = r"UPDATE SC_PLAN SET JdyId = '{1}' WHERE K_ID = '{0}' "

	data_dict = {}

	df = mssql.sqlWork(sqlStr_getPlan)
	print(df)
	# df = data_get.all()
	# print(df.columns)
	print(df.at[1, 'plan_index'])
	# if data_get:
	# 	for index in range(df.shape[0]):
			# plan_index = data_get.loc[[0], [0]]
	# 		# data_dict.update({'plan_index': {'value': plan_index}})
	# 		# responce = api.create_data(data_dict)
	# 		# _id = responce['_id']
	# 		print(plan_index)
	# # 		mssql.sqlWork(sqlStr_setPlan.format(plan_index, _id))


