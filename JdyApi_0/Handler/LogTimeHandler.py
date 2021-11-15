from JdyHelper.JdyApi import APIUtils
from Handler.Logger import Logger
import time, datetime


# 报工记录日志明细表
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
entryId = '60cabc93d11b7e0008b2b7f3'

api = APIUtils(appId, entryId, api_key)

log = Logger('报工记录日志明细表 -- 时间调整')


def main_work():
	log.log()
	# 按条件获取表单数据
	title = ['work_uuid',
	         'insert_time', 'insert_date',
	         'update_time', 'update_date',
	         'final_time', 'final_date',
	         'work_time_type',
	         'process_flag_1', 'process_flag_2',
	         ]

	data_filter = {
		'rel': 'or',
		'cond': [
			api.set_dict_filter('process_flag_1', 'eq', '0'),
			api.set_dict_filter('final_date_stamp_str', 'empty')
		]
	}

	# print(data_filter)

	data = api.get_form_data('', 100, title, data_filter)

	delta1 = datetime.timedelta(hours=-12)
	delta2 = datetime.timedelta(hours=8)
	delta3 = datetime.timedelta(hours=-8)

	# print('按条件获取表单数据：')
	if not data:
		log.log('API返回无数据')
	else:
		log.log('开始处理')
		for tmp in data:
			log.log(tmp)
			_id = tmp['_id']
			work_uuid = tmp['work_uuid']

			insert_time = tmp['insert_time'][:-4]+'000Z'
			update_time = tmp['update_time'][:-4]+'000Z'
			# print(insert_time[:-4]+'000Z')

			insert_date = (datetime.datetime.strptime((datetime.datetime.strptime(insert_time, "%Y-%m-%dT%H:%M:%S.000Z")
				                                          + delta2).strftime("%Y-%m-%dT00:00:00.000Z"),
				                                         "%Y-%m-%dT%H:%M:%S.000Z") + delta3).strftime(
					"%Y-%m-%dT%H:%M:%S.000Z")
			update_date = (datetime.datetime.strptime((datetime.datetime.strptime(update_time, "%Y-%m-%dT%H:%M:%S.000Z")
				                                          + delta2).strftime("%Y-%m-%dT00:00:00.000Z"),
				                                         "%Y-%m-%dT%H:%M:%S.000Z") + delta3).strftime(
					"%Y-%m-%dT%H:%M:%S.000Z")
			insert_time2 = insert_time
			final_time = ''
			final_date = ''

			if tmp['work_time_type'] == '夜班':
				final_time = (datetime.datetime.strptime(insert_time2, "%Y-%m-%dT%H:%M:%S.000Z") + delta1).strftime(
					"%Y-%m-%dT%H:%M:%S.000Z")
				final_date = (datetime.datetime.strptime((datetime.datetime.strptime(final_time, "%Y-%m-%dT%H:%M:%S.000Z")
				                                          + delta2).strftime("%Y-%m-%dT00:00:00.000Z"),
				                                         "%Y-%m-%dT%H:%M:%S.000Z") + delta3).strftime(
					"%Y-%m-%dT%H:%M:%S.000Z")
			else:
				final_time = insert_time
				final_date = insert_date

			# 转化时间戳
			final_date_array_tmp = (datetime.datetime.strptime(final_time, "%Y-%m-%dT%H:%M:%S.000Z") + delta2).strftime("%Y-%m-%d 00:00:00")

			final_date_array = time.strptime(final_date_array_tmp, "%Y-%m-%d %H:%M:%S")

			final_date_stamp_int = int(time.mktime(final_date_array)) * 1000
			final_date_stamp_str = str(final_date_stamp_int)

			update = {}

			api.set_dict_value(update, 'insert_date', insert_date)
			api.set_dict_value(update, 'update_date', update_date)
			api.set_dict_value(update, 'final_time', final_time)
			api.set_dict_value(update, 'final_date', final_date)
			api.set_dict_value(update, 'final_date_stamp_int', final_date_stamp_int)
			api.set_dict_value(update, 'final_date_stamp_str', final_date_stamp_str)
			api.set_dict_value(update, 'process_flag_1', '1')

			result = api.update_data(dataId=_id, data=update)
