from JdyHelper.JdyApi import APIUtils
from BaseHelper import MsSqlHelper
from Handler.Logger import Logger
import datetime


# 报工记录日志明细表
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
entryId = '60cabc93d11b7e0008b2b7f3'

# mssql_url = 'comfort-oa.com:60043'
mssql_url = '192.168.0.99'

api = APIUtils(appId, entryId, api_key)

log = Logger('报工记录日志明细表 -- 排程调整')


def main_work():
	mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')
	log.log()
	# 按条件获取表单数据
	title = ['work_uuid',
	         'order_id', 'plan_order_id',
	         'plan_wlno', 'plan_wlno_name',
	         'plan_wlno_spec', 'plan_wlno_pz', 'plan_wlno_pz_spec', 'plan_wlno_series',
	         'process_flag_1', 'process_flag_2',
	         ]

	data_filter = {
		'rel': 'and',
		'cond': [
			api.set_dict_filter('process_flag_2', 'eq', '0')
		]
	}

	# print(data_filter)

	data = api.get_form_data('', 100, title, data_filter)

	# print('按条件获取表单数据：')
	if not data:
		log.log('API返回无数据')
	else:
		log.log('开始处理')
		for tmp in data:
			log.log(tmp)
			_id = tmp['_id']
			work_uuid = tmp['work_uuid']
			order_id = tmp['order_id']
			plan_order_id = tmp['plan_order_id']
			plan_wlno = tmp['plan_wlno']
			plan_wlno_name = tmp['plan_wlno_name']
			plan_wlno_spec = tmp['plan_wlno_spec']
			plan_wlno_pz = tmp['plan_wlno_pz']
			plan_wlno_pz_spec = tmp['plan_wlno_pz_spec']
			plan_wlno_series = tmp['plan_wlno_series']

			# 排程单号，品号，品名
			plan_order_id = str(order_id).split('(')[0].split('（')[0].replace(' ', '')

			sqlStrWlno = r"SELECT TOP 1 SC028 plan_wlno, SC010 plan_wlno_name, SC012 plan_wlno_spec, " \
			             r"SC015 plan_wlno_pz, SC016 plan_wlno_pz_spec, ISNULL(INVMB.UDF12, '') plan_wlno_series  " \
			             r"FROM SC_PLAN " \
			             r"LEFT JOIN COMFORT.dbo.INVMB ON SC028 = MB001 " \
			             r"WHERE SC001 = '{0}' "
			try:
				if plan_order_id != '':
					sql_get = mssql.sqlWork(sqlStrWlno.format(plan_order_id))
					plan_wlno = sql_get.at[0, 'plan_wlno']
					plan_wlno_name = sql_get.at[0, 'plan_wlno_name']
					plan_wlno_spec = sql_get.at[0, 'plan_wlno_spec']
					plan_wlno_pz = sql_get.at[0, 'plan_wlno_pz']
					plan_wlno_pz_spec = sql_get.at[0, 'plan_wlno_pz_spec']
					plan_wlno_series = sql_get.at[0, 'plan_wlno_series']
			except:
				pass

			update = {}

			api.set_dict_value(update, 'plan_order_id', plan_order_id)
			api.set_dict_value(update, 'plan_wlno', plan_wlno)
			api.set_dict_value(update, 'plan_wlno_name', plan_wlno_name)
			api.set_dict_value(update, 'plan_wlno_spec', plan_wlno_spec)
			api.set_dict_value(update, 'plan_wlno_pz', plan_wlno_pz)
			api.set_dict_value(update, 'plan_wlno_pz_spec', plan_wlno_pz_spec)
			api.set_dict_value(update, 'plan_wlno_series', plan_wlno_series)
			api.set_dict_value(update, 'process_flag_2', '1')

			# print(update)

			result = api.update_data(dataId=_id, data=update)
