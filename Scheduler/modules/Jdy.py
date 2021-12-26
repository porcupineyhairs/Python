from modules.JdyHelper.JdyApi import APIUtils
from modules.SqlHelper import MsSqlHelper
from modules.LogHelper import logger
import datetime
import requests
import json
import time


class DingTalk_Base:
	def __init__(self, url=''):
		self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
		self.url = url
	
	def send_msg(self, text, mobile=[""]):
		json_text = {
			"msgtype": "text",
			"text": {
				"content": text
			},
		}
		if mobile == 'all':
			json_text.update({"at": {
				"atMobiles": mobile,
				"isAtAll": True
			}})
		else:
			json_text.update({"at": {
				"atMobiles": mobile,
				"isAtAll": False
			}})
		return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content


class BasicPlanFix:
	def __init__(self):
		# 排程任务表
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '605d8c522ebb120009ba204a'
		self.entryId = '6051600321802f000703bc71'

		self.mssql_url = 'comfort-oa.com:60043'

		self.api = APIUtils(self.appId, self.entryId, self.api_key)
		self.mssql = MsSqlHelper(host=self.mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')

	def main(self):
		self.__init__()
		# 按条件获取表单数据
		title = ['order_id', 'order_type', 'plan_order_id', 'wlno_other_flag', 'plan_wlno', 'plan_dept',
				 'plan_wlno_name']

		data_filter = {
			'rel': 'or',
			'cond': [
				# api.set_dict_filter('plan_order_id', 'empty'),
				self.api.set_dict_filter('plan_order_id', 'empty'),
				self.api.set_dict_filter('wlno_other_flag', 'empty'),
				self.api.set_dict_filter('wlno_other_flag', 'eq', 'Error')
			]
		}
		data = self.api.get_form_data('', 100, title, data_filter)

		if not data:
			logger.info('排程数据-填充 -- API返回无数据')
		else:
			for tmp in data:
				logger.info('排程数据-填充 -- ' + str(tmp))
				_id = tmp['_id']
				order_id = tmp['order_id']

				if order_id != '':
					update = {}

					# 排程单号，品号，品名
					plan_order_id = str(order_id).split('(')[0].split('（')[0].replace(' ', '')
					plan_order_id_2 = plan_order_id.split('-')[1]

					self.api.set_dict_value(update, 'plan_order_id', plan_order_id)
					self.api.set_dict_value(update, 'plan_order_id_2', plan_order_id_2)

					sqlStrWlno = r"SELECT TOP 1 SC028 plan_wlno, SC010 plan_wlno_name, SC009 plan_po, " \
								 r"SC017 plan_pz_color FROM SC_PLAN WHERE SC001 = '{0}' "
					sqlStrPart = r"exec P_JDY_GetWlnoPartInfo '{0}' "

					try:
						if plan_order_id != '':
							sql_get_wlno = self.mssql.sqlWork(sqlStrWlno.format(plan_order_id))
							sql_get_part = self.mssql.sqlWork(sqlStrPart.format(plan_order_id))

							# 把sql获取到的信息都填入到更新的字典里
							if sql_get_wlno is not None:
								for col in sql_get_wlno.columns:
									self.api.set_dict_value(update, col, sql_get_wlno.at[0, col])
							if sql_get_part is not None:
								for col in sql_get_part.columns:
									self.api.set_dict_value(update, col, sql_get_part.at[0, col])

							# 特殊处理内容
							# 补件标识
							wlno_other_flag = ''
							if sql_get_wlno.at[0, 'plan_wlno'] != '':
								if sql_get_wlno.at[0, 'plan_wlno'].startswith('1'):
									wlno_other_flag = '成品'
								elif sql_get_wlno.at[0, 'plan_wlno'].startswith('2'):
									wlno_other_flag = '补件'
								elif sql_get_wlno.at[0, 'plan_wlno'].startswith('3') or sql_get_wlno.at[
									0, 'plan_wlno'].startswith('4'):
									wlno_other_flag = '原材料'
								else:
									wlno_other_flag = '成品'
							self.api.set_dict_value(update, 'wlno_other_flag', wlno_other_flag)
					except:
						self.api.set_dict_value(update, 'wlno_other_flag', 'Error')
					finally:
						result = self.api.update_data(dataId=_id, data=update)
		del self.mssql


class LogPlanHandler:
	def __init__(self):
		# 报工记录日志明细表
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '605d8c522ebb120009ba204a'
		self.entryId = '60cabc93d11b7e0008b2b7f3'

		self.mssql_url = 'comfort-oa.com:60043'
		# mssql_url = '192.168.0.99'

		self.api = APIUtils(self.appId, self.entryId, self.api_key)
		self.mssql = MsSqlHelper(host=self.mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')

	def main(self):
		self.__init__()
		# 按条件获取表单数据
		title = ['work_uuid',
				 'order_id', 'plan_order_id',
				 'plan_wlno', 'plan_wlno_name',
				 'plan_wlno_spec', 'plan_wlno_pz', 'plan_wlno_pz_spec', 'plan_wlno_series',
				 'process_flag_1', 'process_flag_2', ]

		data_filter = {
			'rel': 'and',
			'cond': [
				self.api.set_dict_filter('process_flag_2', 'eq', '0')
			]
		}

		# print(data_filter)

		data = self.api.get_form_data('', 100, title, data_filter)

		# print('按条件获取表单数据：')
		if not data:
			logger.info('报工日志-排程调整 -- API返回无数据')
		else:
			for tmp in data:
				logger.info('报工日志-排程调整 -- ' + str(tmp))
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
						sql_get = self.mssql.sqlWork(sqlStrWlno.format(plan_order_id))
						plan_wlno = sql_get.at[0, 'plan_wlno']
						plan_wlno_name = sql_get.at[0, 'plan_wlno_name']
						plan_wlno_spec = sql_get.at[0, 'plan_wlno_spec']
						plan_wlno_pz = sql_get.at[0, 'plan_wlno_pz']
						plan_wlno_pz_spec = sql_get.at[0, 'plan_wlno_pz_spec']
						plan_wlno_series = sql_get.at[0, 'plan_wlno_series']
				except:
					pass

				update = {}

				self.api.set_dict_value(update, 'plan_order_id', plan_order_id)
				self.api.set_dict_value(update, 'plan_wlno', plan_wlno)
				self.api.set_dict_value(update, 'plan_wlno_name', plan_wlno_name)
				self.api.set_dict_value(update, 'plan_wlno_spec', plan_wlno_spec)
				self.api.set_dict_value(update, 'plan_wlno_pz', plan_wlno_pz)
				self.api.set_dict_value(update, 'plan_wlno_pz_spec', plan_wlno_pz_spec)
				self.api.set_dict_value(update, 'plan_wlno_series', plan_wlno_series)
				self.api.set_dict_value(update, 'process_flag_2', '1')

				result = self.api.update_data(dataId=_id, data=update)
		del self.mssql


class LogTimeHandler:
	def __init__(self):
		# 报工记录日志明细表
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '605d8c522ebb120009ba204a'
		self.entryId = '60cabc93d11b7e0008b2b7f3'

		self.api = APIUtils(self.appId, self.entryId, self.api_key)

	def main(self):
		self.__init__()
		# 按条件获取表单数据
		title = ['work_uuid',
				 'insert_time', 'insert_date',
				 'update_time', 'update_date',
				 'final_time', 'final_date',
				 'work_time_type',
				 'process_flag_1', 'process_flag_2']

		data_filter = {
			'rel': 'or',
			'cond': [
				self.api.set_dict_filter('process_flag_1', 'eq', '0'),
				self.api.set_dict_filter('final_date_stamp_str', 'empty')
			]
		}

		data = self.api.get_form_data('', 100, title, data_filter)

		delta1 = datetime.timedelta(hours=-12)
		delta2 = datetime.timedelta(hours=8)
		delta3 = datetime.timedelta(hours=-8)

		# print('按条件获取表单数据：')
		if not data:
			logger.info('报工日志-时间调整 -- API返回无数据')
		else:
			for tmp in data:
				logger.info('报工日志-时间调整 -- ' + str(tmp))
				_id = tmp['_id']
				work_uuid = tmp['work_uuid']

				insert_time = tmp['insert_time'][:-4] + '000Z'
				update_time = tmp['update_time'][:-4] + '000Z'
				# print(insert_time[:-4]+'000Z')

				insert_date = (datetime.datetime.strptime(
					(datetime.datetime.strptime(insert_time, "%Y-%m-%dT%H:%M:%S.000Z")
					 + delta2).strftime("%Y-%m-%dT00:00:00.000Z"),
					"%Y-%m-%dT%H:%M:%S.000Z") + delta3).strftime(
					"%Y-%m-%dT%H:%M:%S.000Z")
				update_date = (datetime.datetime.strptime(
					(datetime.datetime.strptime(update_time, "%Y-%m-%dT%H:%M:%S.000Z")
					 + delta2).strftime("%Y-%m-%dT00:00:00.000Z"),
					"%Y-%m-%dT%H:%M:%S.000Z") + delta3).strftime(
					"%Y-%m-%dT%H:%M:%S.000Z")
				insert_time2 = insert_time
				final_time = ''
				final_date = ''

				if tmp['work_time_type'] == '夜班':
					final_time = (datetime.datetime.strptime(insert_time2, "%Y-%m-%dT%H:%M:%S.000Z") + delta1).strftime(
						"%Y-%m-%dT%H:%M:%S.000Z")
					final_date = (datetime.datetime.strptime(
						(datetime.datetime.strptime(final_time, "%Y-%m-%dT%H:%M:%S.000Z")
						 + delta2).strftime("%Y-%m-%dT00:00:00.000Z"),
						"%Y-%m-%dT%H:%M:%S.000Z") + delta3).strftime(
						"%Y-%m-%dT%H:%M:%S.000Z")
				else:
					final_time = insert_time
					final_date = insert_date

				# 转化时间戳
				final_date_array_tmp = (
							datetime.datetime.strptime(final_time, "%Y-%m-%dT%H:%M:%S.000Z") + delta2).strftime(
					"%Y-%m-%d 00:00:00")

				final_date_array = time.strptime(final_date_array_tmp, "%Y-%m-%d %H:%M:%S")

				final_date_stamp_int = int(time.mktime(final_date_array)) * 1000
				final_date_stamp_str = str(final_date_stamp_int)

				update = {}

				self.api.set_dict_value(update, 'insert_date', insert_date)
				self.api.set_dict_value(update, 'update_date', update_date)
				self.api.set_dict_value(update, 'final_time', final_time)
				self.api.set_dict_value(update, 'final_date', final_date)
				self.api.set_dict_value(update, 'final_date_stamp_int', final_date_stamp_int)
				self.api.set_dict_value(update, 'final_date_stamp_str', final_date_stamp_str)
				self.api.set_dict_value(update, 'process_flag_1', '1')

				result = self.api.update_data(dataId=_id, data=update)


class GetRobotGxSumHandler:
	def __init__(self):
		# 加工部报工-其他
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '605d8c522ebb120009ba204a'

		self.mssql_url = 'comfort-oa.com:60043'
		self.mssql = MsSqlHelper(host=self.mssql_url, user='sa', passwd='comfortgroup2016{', database='WG_DB')

		self.delta = datetime.timedelta(hours=+8)

	def main(self):
		self.__init__()
		self.work1()
		self.work2()
		del self.mssql

	def work1(self):
		entryId = '60d42d37eac4360008cf56c1'
		api = APIUtils(self.appId, entryId, self.api_key)
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
			logger.info('加工报工-披覆自动化 -- API返回无数据')
		else:
			for tmp in data:
				logger.info('加工报工-披覆自动化 -- ' + str(tmp))
				_id = tmp['_id']
				plan_date = (datetime.datetime.strptime(tmp['plan_date'][:-4] + '000Z',
														"%Y-%m-%dT%H:%M:%S.000Z") + self.delta).strftime("%Y%m%d")

				# 清空子表单内容
				update = {}
				api.set_dict_value(update, 'data_detail', [])
				result = api.update_data(dataId=_id, data=update)

				df = self.mssql.sqlWork(sqlStr.format(plan_date))
				detail_sum = []
				if df is not None:
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

	def work2(self):
		entryId = '60d57131e9795d0009f4cf41'
		api = APIUtils(self.appId, entryId, self.api_key)
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
			logger.info('加工报工-加工自动化 -- API返回无数据')
		else:
			for tmp in data:
				logger.info('加工报工-加工自动化 -- ' + str(tmp))
				_id = tmp['_id']
				plan_date = (datetime.datetime.strptime(tmp['plan_date'][:-4] + '000Z',
														"%Y-%m-%dT%H:%M:%S.000Z") + self.delta).strftime("%Y%m%d")

				# 清空子表单内容
				update = {}
				api.set_dict_value(update, 'data_detail', [])
				result = api.update_data(dataId=_id, data=update)

				df = self.mssql.sqlWork(sqlStr.format(plan_date))
				detail_sum = []
				if df is not None:
					detail_sum = []
					for row in range(df.shape[0]):
						detail = {}
						for col in df.columns:
							api.set_dict_value(detail, col, df.at[row, col])
						detail_sum.append(detail)

				# 填充子表单内容
				update = {}
				api.set_dict_value(update, 'data_detail', detail_sum)
				api.set_dict_value(update, 'process_flag', '1')
				result = api.update_data(dataId=_id, data=update)


class BasicPlanErrorAlert:
	def __init__(self):
		# 排程任务表
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '605d8c522ebb120009ba204a'
		self.entryId = '6051600321802f000703bc71'
		self.api = APIUtils(self.appId, self.entryId, self.api_key)
		self.ding = DingTalk_Base(url='https://oapi.dingtalk.com/robot/send?access_token=e82d83db5417257c58cb31d3abb4c9e59f00dc341d1ec4bf00f4caacb9ae3660')
		
	def main(self):
		self.__init__()
		self.work1()
	
	def work1(self):
		# 按条件获取表单数据
		title = ['order_id', 'order_type', 'plan_order_id', 'wlno_other_flag', 'plan_wlno', 'plan_dept',
		         'plan_wlno_name']
		
		data_filter = {
			'rel': 'or',
			'cond': [
				self.api.set_dict_filter('plan_index0', 'empty'),
				self.api.set_dict_filter('order_id', 'empty'),
				self.api.set_dict_filter('plan_dept', 'empty'),
			]
		}
		data = self.api.get_form_data('', 1000, title, data_filter)
		if not data:
			logger.info('排程数据-异常 -- API返回无数据')
		else:
			data_len = len(data)
			msg = '简道云-排程任务表，共有{data_len}笔异常(唯一序号|生产单号|生产组别 为空)'.format(data_len=data_len)
			logger.info('排程数据-异常 -- ' + msg)
			self.ding.send_msg(msg, 'all')
