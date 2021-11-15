import dingtalk
from SqlHelper import MsSqlHelper
import jsonextend
# from apscheduler.schedulers.blocking import BlockingScheduler
import json

# scheduler = BlockingScheduler()
sql = MsSqlHelper(host='comfort-hr.com', user='sa', passwd='WjzcomFort@2019', database='HYHRV3')

app_key = "dingf8vlo9vvq0vqn84x"
app_secret = "PsAfaIWVe58ukgsvaBXHOxX0aW0LqUT5E54XmPDfXgzlL0srOVfnEDBIXBM4kLsg"
corp_id = "1045238247"
op_userid = "01180666186637615720"
client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)

# vacation type list
def type_list():
	# client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	info = client.vacation.type_list(op_userid=op_userid)
	print(info)
	pass


def list_by_user_id_basic(offset=0, size=100):
	info = client.bpms.process_listbyuserid(userid=op_userid, offset=offset, size=size)
	return info


def list_by_user_id():
	flag = True
	offset = 0
	process_top_vo = []
	while flag:
		info = list_by_user_id_basic(offset)
		try:
			next_cursor = info['next_cursor']
		except:
			next_cursor = 0

		process_list = info['process_list']
		process_top_vo.extend(process_list['process_top_vo'])

		if next_cursor != 0 :
			offset += 1
		else:
			flag = False
		# print(next_cursor, offset)
		# print(len(process_top_vo))
	return process_top_vo


def get_process_code_single(process_top_vo, name=''):
	codes = ''
	for process_top_vo_tmp in process_top_vo:
		if process_top_vo_tmp['name'] == name:
			codes = process_top_vo_tmp['process_code']
			break
	return codes


def get_process_code():
	process_code = [{'name': '请假', 'code':''},
					{'name': '出差', 'code':''},
					{'name': '加班', 'code':''},
					{'name': '补卡申请', 'code':''}]

	process_code_new = []
	process_top_vo = list_by_user_id()
	if len(process_top_vo) > 0:
		for process_code_tmp in process_code:
			name = process_code_tmp['name']
			codes = get_process_code_single(process_top_vo, name)
			process_code_new.append({'name': name, 'code': codes})

	print(process_code_new)


def process_instance_list(process_code, start_time, end_time, cursor, size=20):
	pass


def get_process_list():
	codes = 'PROC-78444D64-A18D-4E2B-84BE-A7493A50A3F0'


# 查看单个流程实例
def process_instance_get():
	process_codes = 'PROC-78444D64-A18D-4E2B-84BE-A7493A50A3F0'
	process_instance_id = '7d703e9c-48bf-4c8d-8e5c-ab7ac5571e7a'
	info = client.bpms.processinstance_get(process_instance_id)
	# info2 = jsonextend.dict_generator(info)
	sjson = json.dumps(info)
	print(sjson)


if __name__ == '__main__':
	# get_process_code()
	process_instance_get()
