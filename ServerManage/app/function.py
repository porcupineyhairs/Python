import os


class ProgramStatusInfo:
	@staticmethod
	def get_status(program_name):
		active = ''
		status = ''
		pid = ''
		enable = False
		
		if program_name.count('.service') <= 0:
			program_name += '.service'

		active, status = ProgramStatusInfo.get_active(program_name)
		if active == 'Active':
			pid = ProgramStatusInfo.get_pid(program_name)
		enable = ProgramStatusInfo.get_enable(program_name)
		return active, status, pid, enable
	
	@staticmethod
	def get_active(program_name):
		status_str = 'systemctl status {program_name} |grep Active '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		cmd_rtn = os.popen(status_str.format(program_name=program_name), 'r')
		rtn_str = cmd_rtn.read()
		rtn_str_list = rtn_str.strip().split(' ')
		if rtn_str != '':
			return rtn_str_list[1].title(), rtn_str_list[2].title().strip('(').strip(')')
		else:
			return '', ''
			
	@staticmethod
	def get_pid(program_name):
		status_str = 'systemctl status {program_name} |grep PID '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		cmd_rtn = os.popen(status_str.format(program_name=program_name), 'r')
		rtn_str = cmd_rtn.read()
		rtn_str_list = rtn_str.strip().split(' ')
		return rtn_str_list[2]
		
	@staticmethod
	def get_enable(program_name):
		enable_str = 'ls /etc/systemd/system/multi-user.target.wants | grep  {program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		cmd_rtn = os.popen(enable_str.format(program_name=program_name), 'r')
		rtn_str = cmd_rtn.read().strip()
		return True if rtn_str != '' else False
		
	@staticmethod
	def get_service_file(program_name):
		file_str = 'cat /usr/lib/systemd/system/{program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		cmd_rtn = os.popen(file_str.format(program_name=program_name), 'r')
		rtn_str = cmd_rtn.read()
		return rtn_str
	
	@staticmethod
	def set_start(program_name):
		set_str = 'systemctl {set} {program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		os.popen(set_str.format(set='start', program_name=program_name), 'r')
	
	@staticmethod
	def set_stop(program_name):
		set_str = 'systemctl {set} {program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		os.popen(set_str.format(set='stop', program_name=program_name), 'r')
	
	@staticmethod
	def set_restart(program_name):
		set_str = 'systemctl {set} {program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		os.popen(set_str.format(set='restart', program_name=program_name), 'r')
		
	@staticmethod
	def set_enable(program_name):
		set_str = 'systemctl {set} {program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		os.popen(set_str.format(set='enable', program_name=program_name), 'r')
	
	@staticmethod
	def set_disable(program_name):
		set_str = 'systemctl {set} {program_name} '
		if program_name.count('.service') <= 0:
			program_name += '.service'
		os.popen(set_str.format(set='disable', program_name=program_name), 'r')
