from JdyHelper.JdyApi import APIUtils
from BaseHelper import MsSqlHelper
from Handler.Logger import Logger
import datetime


# 排程任务表
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
entryId = '6051600321802f000703bc71'

# mssql_url = 'comfort-oa.com:60043'
mssql_url = '192.168.0.99'

api = APIUtils(appId, entryId, api_key)

log = Logger('排程任务表 -- 排程基础数据填充')


def main_work():
	mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')
	log.log()
	# 按条件获取表单数据
	field = ['order_id', 'order_type', 'plan_order_id', 'wlno_other_flag', 'plan_wlno', 'plan_dept', 'plan_wlno_name',
	         ]

	data_filter = {
		'rel': 'and',
		'cond': [
			# api.set_dict_filter('plan_order_id', 'empty'),
			api.set_dict_filter('plan_order_id', 'empty'),
			# api.set_dict_filter('order_type', 'eq', '外销'),
			api.set_dict_filter('order_id', 'not_empty')
		]
	}
	data = api.get_form_data('', 100, field, data_filter)

	# print('按条件获取表单数据：')
	if not data:
		log.log('API返回无数据')
	else:
		log.log('开始处理')
		for tmp in data:
			log.log(tmp)
			_id = tmp['_id']
			order_id = tmp['order_id']

			update = {}

			# 排程单号，品号，品名
			plan_order_id = str(order_id).split('(')[0].split('（')[0].replace(' ', '')
			plan_order_id_2 = plan_order_id.split('-')[1]

			api.set_dict_value(update, 'plan_order_id', plan_order_id)
			api.set_dict_value(update, 'plan_order_id_2', plan_order_id_2)

			sqlStrWlno = r"SELECT TOP 1 SC028 plan_wlno, SC010 plan_wlno_name, SC009 plan_po, SC017 plan_pz_color FROM SC_PLAN WHERE SC001 = '{0}' "
			sqlStrPart = r"exec P_JDY_GetWlnoPartInfo '{0}' "

			try:
				if plan_order_id != '':
					sql_get_wlno = mssql.sqlWork(sqlStrWlno.format(plan_order_id))
					sql_get_part = mssql.sqlWork(sqlStrPart.format(plan_order_id))

					# 把sql获取到的信息都填入到更新的字典里
					if sql_get_wlno is not None:
						for col in sql_get_wlno.columns:
							api.set_dict_value(update, col, sql_get_wlno.at[0, col])
					if sql_get_part is not None:
						for col in sql_get_part.columns:
							api.set_dict_value(update, col, sql_get_part.at[0, col])

					# 特殊处理内容
					# 补件标识
					wlno_other_flag = ''
					if sql_get_wlno.at[0, 'plan_wlno'] != '':
						if sql_get_wlno.at[0, 'plan_wlno'].startswith('1') and 'LPO' in sql_get_wlno.at[0, 'plan_wlno_name']:
							wlno_other_flag = '补件'
						elif sql_get_wlno.at[0, 'plan_wlno'].startswith('2'):
							wlno_other_flag = '补件'
						elif sql_get_wlno.at[0, 'plan_wlno'].startswith('3'):
							wlno_other_flag = '原材料'
						else:
							wlno_other_flag = '成品'
					api.set_dict_value(update, 'wlno_other_flag', wlno_other_flag)
			except:
				pass
			finally:
				result = api.update_data(dataId=_id, data=update)
