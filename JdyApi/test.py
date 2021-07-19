from JdyHelper.JdyApi import APIUtils
from Handler.Logger import Logger
import datetime


# 报工记录日志明细表
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
entryId = '60cabc93d11b7e0008b2b7f3'

api = APIUtils(appId, entryId, api_key)

log = Logger('报工记录日志明细表 -- 测试')


def main_work():
	log.log()
	# 按条件获取表单数据
	title = ['work_uuid',
	         'work_dept', 'work_group',
	         'work_line', 'work_part',
	         'work_time_type'
	         ]

	data_filter = {
		'rel': 'and',
		'cond': [
			api.set_dict_filter('work_dept', 'eq', '加工部'),
			api.set_dict_filter('work_group', 'eq', '加工组-背垫'),
			# api.set_dict_filter('work_part', 'eq', '腰'),
			api.set_dict_filter('process_flag_1', 'eq', '1'),
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

			update = {}

			api.set_dict_value(update, 'work_group', '背垫加工')

			result = api.update_data(dataId=_id, data=update)


if __name__ == '__main__':
	main_work()
