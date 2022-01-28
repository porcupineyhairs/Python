import os


class ProgramStatusInfo:
	status_str = 'systemctl status {program_name} |grep {cmd_keyword} '
	enable_str = 'ls /etc/systemd/system/multi-user.target.wants | grep  {program_name} '
	set_str = 'systemctl {set} {program_name} '
	program_name = ''

	active = ''
	status = ''
	pid = ''
	enable = False

	def get_status(self, program_name):
		self.program_name = program_name
		self.status = ''
		self.pid = ''
		if self.program_name.count('.service') < 0:
			self.program_name += '.service'

		self.__get_active()
		if self.active == 'Active':
			self.__get_pid()
		self.__get_enable()
		return self.active, self.status, self.pid, self.enable

	def __get_active(self):
		cmd_keyword = 'Active'
		cmd_rtn = os.popen(self.status_str.format(program_name=self.program_name, cmd_keyword=cmd_keyword), 'r')
		rtn_str = cmd_rtn.read()
		rtn_str_list = rtn_str.strip().split(' ')
		if rtn_str != '':
			self.active = rtn_str_list[1].title()
			self.status = rtn_str_list[2].title().strip('(').strip(')')

	def __get_pid(self):
		cmd_keyword = 'PID'
		cmd_rtn = os.popen(self.status_str.format(program_name=self.program_name, cmd_keyword=cmd_keyword), 'r')
		rtn_str = cmd_rtn.read()
		rtn_str_list = rtn_str.strip().split(' ')
		self.pid = rtn_str_list[2]
		
	def __get_enable(self):
		cmd_rtn = os.popen(self.enable_str.format(program_name=self.program_name), 'r')
		rtn_str = cmd_rtn.read().strip()
		self.enable = True if rtn_str != '' else False
	
	def set_start(self, program_name):
		if program_name.count('.service') < 0:
			program_name += '.service'
		os.popen(self.set_str.format(set='start', program_name=program_name), 'r')
	
	def set_stop(self, program_name):
		if program_name.count('.service') < 0:
			program_name += '.service'
		os.popen(self.set_str.format(set='stop', program_name=program_name), 'r')

	def set_restart(self, program_name):
		if program_name.count('.service') < 0:
			program_name += '.service'
		os.popen(self.set_str.format(set='restart', program_name=program_name), 'r')
		
	def set_enable(self, program_name):
		if program_name.count('.service') < 0:
			program_name += '.service'
		os.popen(self.set_str.format(set='enable', program_name=program_name), 'r')
	
	def set_disable(self, program_name):
		if program_name.count('.service') < 0:
			program_name += '.service'
		os.popen(self.set_str.format(set='disable', program_name=program_name), 'r')
