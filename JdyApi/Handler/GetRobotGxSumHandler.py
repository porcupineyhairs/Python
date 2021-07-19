from JdyHelper.JdyApi import APIUtils
from BaseHelper import MsSqlHelper
from Handler.Logger import Logger
import datetime


# 加工部报工-其他
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
# entryId = '60d42d37eac4360008cf56c1'

# mssql_url = 'comfort-oa.com:60043'
mssql_url = '192.168.0.99'

delta = datetime.timedelta(hours=+8)

log1 = Logger('报工-加工部披覆自动化')
log2 = Logger('报工-加工部加工自动化')


def main_work():
	work1()
	work2()


# 加工部披覆自动化报工
def work1():
	entryId = '60d42d37eac4360008cf56c1'
	api = APIUtils(appId, entryId, api_key)
	log1.log()
	mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')
	sqlStr = r"EXEC P_JDY_GetRobotGxSum '{0}' "

	# 按条件获取表单数据
	title = ['plan_date', 'data_detail']

	data_filter = {
		'rel': 'and',
		'cond': [
			api.set_dict_filter('process_flag', 'eq', '0')
		]
	}

	data = api.get_form_data('', 100, title, data_filter)

	# print('按条件获取表单数据：')
	if not data:
		log1.log('API返回无数据')
	else:
		log1.log('开始处理')

		for tmp in data:
			# print(tmp)
			_id = tmp['_id']
			plan_date = (datetime.datetime.strptime(tmp['plan_date'][:-4]+'000Z', "%Y-%m-%dT%H:%M:%S.000Z") + delta).strftime(
					"%Y%m%d")
			log1.log(plan_date)

			# 清空子表单内容
			update = {}
			api.set_dict_value(update, 'data_detail', [])
			result = api.update_data(dataId=_id, data=update)

			df = mssql.sqlWork(sqlStr.format(plan_date))
			detail_sum = []
			if len(df):
				# print(df)
				# print(df.at[1, 'wlno_series'])
				detail_sum = []
				for row in range(df.shape[0]):
					detail = {}
					for col in df.columns:
						api.set_dict_value(detail, col, df.at[row, col])
					detail_sum.append(detail)
				# print(detail_sum)

			# 填充子表单内容
			update = {}
			api.set_dict_value(update, 'data_detail', detail_sum)
			api.set_dict_value(update, 'process_flag', '1')
			# print(update)
			result = api.update_data(dataId=_id, data=update)


# 加工部加工报工
def work2():
	entryId = '60d57131e9795d0009f4cf41'
	api = APIUtils(appId, entryId, api_key)
	log2.log()
	mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')
	sqlStr = r"EXEC P_JDY_GetRobotGxSum2 '{0}' "

	# 按条件获取表单数据
	title = ['plan_date', 'data_detail']

	data_filter = {
		'rel': 'and',
		'cond': [
			api.set_dict_filter('process_flag', 'eq', '0')
		]
	}

	data = api.get_form_data('', 100, title, data_filter)

	# print('按条件获取表单数据：')
	if not data:
		log2.log('API返回无数据')
	else:
		log2.log('开始处理')

		for tmp in data:
			# print(tmp)
			_id = tmp['_id']
			plan_date = (datetime.datetime.strptime(tmp['plan_date'][:-4]+'000Z', "%Y-%m-%dT%H:%M:%S.000Z") + delta).strftime(
					"%Y%m%d")
			log2.log(plan_date)

			# 清空子表单内容
			update = {}
			api.set_dict_value(update, 'data_detail', [])
			result = api.update_data(dataId=_id, data=update)

			df = mssql.sqlWork(sqlStr.format(plan_date))
			detail_sum = []
			if len(df):
				# print(df)
				# print(df.at[1, 'wlno_series'])
				detail_sum = []
				for row in range(df.shape[0]):
					detail = {}
					for col in df.columns:
						api.set_dict_value(detail, col, df.at[row, col])
					detail_sum.append(detail)
				# print(detail_sum)

			# 填充子表单内容
			update = {}
			api.set_dict_value(update, 'data_detail', detail_sum)
			api.set_dict_value(update, 'process_flag', '1')
			# print(update)
			result = api.update_data(dataId=_id, data=update)
