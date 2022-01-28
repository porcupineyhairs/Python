import os
from app.function import ProgramStatusInfo


def main():
	# cmd_rtn = os.popen('systemctl status flaskserver_python.service |grep Active ', 'r')
	# rtn_str = cmd_rtn.read()
	# rtn_str_list = rtn_str.strip().split(' ')
	# status = rtn_str_list[1] + rtn_str_list[2]
	#
	# print(status)
	# os.system('systemctl stop webserver_python.service ')
	# info = os.system('systemctl status flaskserver_python.service |grep Active ')
	# print(info)
	# os.system('systemctl start djangoserver_python.service ')
	# info = os.system('systemctl status flaskserver_python.service |grep Active ')
	# print(info)

	# subp = subprocess.Popen('systemctl status flaskserver_python.service |grep Active ',
	#                         shell=True,
	#                         # stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
	#                         )
	# subp.wait(2)
	# if subp.poll() == 0:
	# 	print(subp.communicate()[1])
	# else:
	# 	print("失败")

	program_status_info = ProgramStatusInfo()
	get = program_status_info.get_status('flaskserver2_python')
	print(get)


if __name__ == '__main__':
	main()
