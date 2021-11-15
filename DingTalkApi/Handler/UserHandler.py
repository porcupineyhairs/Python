import dingtalk
from SqlHelper import MsSqlHelper


class User:
	def __init__(self):
		self.__dd_app_key = "dings4y1o268lz7a1tui"
		self.__dd_app_secret = "siZV69D95QZQaozl4wKrPF5cMp3eaS9xIfL04PH5QT2rQY-gHYd-ia915gnm3AnO"
		self.__dd_corp_id = "1143998841"
		self.__hr_sql = MsSqlHelper(host='comfort-hr.com', user='sa', passwd='WjzcomFort@2019', database='HYHRV3')
		self.__dd_client = dingtalk.AppKeyClient(corp_id=self.__dd_corp_id,
												 app_key=self.__dd_app_key,
												 app_secret=self.__dd_app_secret)

		self.hr_user_name = None
		self.hr_mobile = None
		self.hr_user_id = None
		self.hr_user_code = None
		self.hr_isactive = None
		self.hr_is_entry = None
		self.hr_ischange_dd = None

		self.dd_user_id = None
		self.dd_user_name = None
		self.dd_user_position = None
		self.dd_user_code = None
		self.dd_user_mobile = None
		self.__clean()

	def __del__(self):
		self.__dd_app_key = None
		self.__dd_app_secret = None
		self.__dd_corp_id = None
		self.__hr_sql = None
		self.__dd_client = None
		self.__clean()

	# 清除信息资料，避免数据残留
	def __clean(self):
		self.hr_user_name = None
		self.hr_mobile = None
		self.hr_user_id = None
		self.hr_user_code = None
		self.hr_isactive = None
		self.hr_is_entry = None
		self.hr_ischange_dd = None

		self.dd_user_id = None
		self.dd_user_name = None
		self.dd_user_position = None
		self.dd_user_code = None
		self.dd_user_mobile = None

	# 执行前预处理，避免数据库连接断开，API断开等情况
	def __pre_work(self):
		self.__clean()

	# 获取钉钉上的人员信息
	def __get_dd_info_authcode(self, auth_code):
		self.__pre_work()
		info = self.__dd_client.user.getuserinfo(auth_code)
		# print(info)
		self.dd_user_id = info['userid']

	def __get_dd_info(self):
		info = self.__dd_client.user.get(self.dd_user_id)
		print(info)
		self.dd_user_name = info['name']
		self.dd_user_position = info['position']
		self.dd_user_code = info['jobnumber']
		self.dd_user_mobile = info['mobile']

	# 获取人员信息
	def get_user_info(self):
		pass

	# 获取HR上的人员信息
	def get_hr_info(self):
		__sql_str = r"SELECT top 1 empid, empcode, empname, mobilephone, isactive, dd_id, is_entry, ischange_dd " \
				   r"from tps_empinfo where empcode = '{user_code}'"
		__data = self.__hr_sql.sqlWork(__sql_str.format(user_code=self.hr_user_code))
		if len(__data) > 0:
			self.hr_mobile = __data.at[0, 'mobilephone']
			self.hr_user_name = __data.at[0, 'empname']
			self.hr_user_id = __data.at[0, 'dd_id']
			self.hr_isactive = __data.at[0, 'isactive']
			self.hr_is_entry = __data.at[0, 'is_entry']
			self.hr_ischange_dd = __data.at[0, 'ischange_dd']

	# 重置HR上关于钉钉的资料
	def set_clean_hr_info(self):
		__sql_str = r"update tps_empinfo set is_entry = 0, ischange_dd = 1, dd_id = null " \
					r"from tps_empinfo where empcode = '{user_code}' and isactive = 1"
		self.__hr_sql.sqlWork(__sql_str.format(user_code=self.hr_user_code))

	# 在钉钉上删除人员信息
	def set_del_dd_info(self, dd_user_id):
		pass

	# 检测未同步到钉钉的人员，并作预入职
	def set_new_dd_info(self):
		pass
