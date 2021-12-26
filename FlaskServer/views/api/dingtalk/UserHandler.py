import dingtalk
from modules.SqlHelper import MsSqlHelper
import datetime


class DdUser:
	def __init__(self, root_path):
		self.__dd_app_key = "dingxnekg2ap7cqgcyuz"
		self.__dd_app_secret = "oclwNjy_l6z_6kWGaUxzsok3ZZXgHOOmtEvleyJFWSrtxuflVo_sWJ-qHtTrCKpR"
		self.__dd_corp_id = "1143998841"
		self.__dd_op_user = '01180666186637615720'
		self.__hr_sql = MsSqlHelper(host='comfort-hr.com', user='sa', passwd='WjzcomFort@2019', database='HYHRV3')
		self.__dd_client = dingtalk.AppKeyClient(corp_id=self.__dd_corp_id,
												 app_key=self.__dd_app_key,
												 app_secret=self.__dd_app_secret)

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
		pass

	# 执行前预处理，避免数据库连接断开，API断开等情况
	def __pre_work(self):
		self.__clean()

	# 根据AuthCode获取钉钉上的人员信息
	def get_dd_user_info_by_authcode(self, auth_code):
		self.__pre_work()
		info = self.__dd_client.user.getuserinfo(auth_code)
		if len(info) > 0:
			dd_user_id = info['userid']
			result = self.__get_dd_user_info(dd_user_id)
			return result
		else:
			return {}

	# 获取人员信息
	def get_user_info(self, hr_user_code):
		result = {'hr_user_id': ''}
		result.update(self.__get_hr_user_info(hr_user_code))
		hr_user_id = result['hr_user_id']
		result.update(self.__get_dd_user_info(hr_user_id))
		result.update(self.get_dd_user_pre_entry(hr_user_id))
		return result

	# 人员是否在待确认到岗名单中
	def get_dd_user_pre_entry(self, dd_user_id):
		result = {'dd_pre_entry_flag': False}
		if dd_user_id != '':
			result.update({'dd_pre_entry_flag': True if dd_user_id in self.__get_dd_user_pre_entry_list() else False})
		return result

	# 对未同步到钉钉的人员同步到钉钉，作预入职
	def set_dd_new_info_by_user_code(self, hr_user_code):
		result = {'result': False}
		try:
			status = self.__set_dd_new_info(hr_user_code)
			result.update({'result': status})
		except Exception as e:
			# print(str(e))
			pass
		return result

	def set_dd_del_info_by_user_code(self, hr_user_code):
		result = {'result': False}
		info = self.__get_hr_user_info(hr_user_code)
		hr_user_id = info['hr_user_id']
		try:
			self.__set_dd_del_info(hr_user_id)
			self.__set_hr_del_dd_info(hr_user_code)
			result.update({'result': True})
		except Exception as e:
			# print(str(e))
			pass
		return result

	def set_dd_update_info_by_user_code(self, hr_user_code):
		result = {'result': False}
		try:
			self.__set_dd_user_info_update(hr_user_code)
			result.update({'result': True})
		except Exception as e:
			# print(str(e))
			pass
		return result

	def __get_dd_user_info(self, dd_user_id):
		result = {'dd_flag': False}
		try:
			if dd_user_id != '':
				info = self.__dd_client.user.get(dd_user_id)
				# print(info)
				if len(info) > 0:
					result.update({'dd_flag': True})
					result.update({'dd_user_name': info.get('name', '')})
					result.update({'dd_user_id': info.get('userid', '')})
					result.update({'dd_user_position': info.get('position', '')})
					result.update({'dd_user_jobnumber': info.get('jobnumber', '')})
					result.update({'dd_user_mobile': info.get('mobile', '')})
					result.update({'dd_department': info.get('department', [])})

					result.update({'dd_department_name': self.__get_dd_user_dept_info(result.get('dd_department', []))})
					result.update({'dd_department_name_full': self.__get_dd_user_dept_info(result.get('dd_department', []),
																						   full=True)})

					extattr = info.get('extattr', None)
					dd_user_erp_id = '' if extattr is None else extattr.get('ERP账号', '')
					dd_user_sort_mobile = '' if extattr is None else extattr.get('手机短号', '')
					result.update({'dd_user_erp_id': dd_user_erp_id})
					result.update({'dd_user_sort_mobile': dd_user_sort_mobile})
		except Exception as e:
			# print(str(e))
			pass
		return result

	# 获取HR上的人员信息
	def __get_hr_user_info(self, hr_user_code):
		__sql_str = r"SELECT top 1 empid, empcode, empname, mobilephone, isactive, dd_id, is_entry, ischange_dd " \
				   r"from tps_empinfo where empcode = '{user_code}'"
		result = {'hr_flag': False}
		if hr_user_code != '':
			data = self.__hr_sql.sqlWork(__sql_str.format(user_code=hr_user_code))
			if data is not None:
				result.update({'hr_flag': True})
				result.update({'hr_user_code': data.at[0, 'empcode']})
				result.update({'hr_user_mobile': data.at[0, 'mobilephone']})
				result.update({'hr_user_name': data.at[0, 'empname']})
				result.update({'hr_user_id': data.at[0, 'dd_id']})
				result.update({'hr_isactive': bool(data.at[0, 'isactive'])})
				result.update({'hr_is_entry': bool(data.at[0, 'is_entry'])})
				result.update({'hr_ischange_dd': bool(data.at[0, 'ischange_dd'])})
		return result

	# 通过部门ID获取部门名称
	def __get_dd_user_dept_info(self, dd_dept_id, full=False):
		if full:
			if isinstance(dd_dept_id, list):
				result = []
				for dd_dept_id_tmp in dd_dept_id:
					parent_dept_list = self.__dd_client.department.list_parent_depts_by_dept(dd_dept_id_tmp)
					parent_dept_list.reverse()
					if len(parent_dept_list) > 0:
						parent_dept_name_list = self.__get_dd_user_dept_info(parent_dept_list, full=False)
						parent_dept_name_list = '/'.join(name for name in parent_dept_name_list)
						result.append(parent_dept_name_list)
				return result
			if isinstance(dd_dept_id, int):
				parent_dept_list = self.__dd_client.department.list_parent_depts_by_dept(dd_dept_id)
				parent_dept_list.reverse()
				parent_dept_name_list = ''
				if len(parent_dept_list) > 0:
					parent_dept_name_list = self.__get_dd_user_dept_info(parent_dept_list, full=False)
					parent_dept_name_list = '/'.join(name for name in parent_dept_name_list)
				return parent_dept_name_list
		else:
			if isinstance(dd_dept_id, list):
				result = []
				for dd_dept_id_tmp in dd_dept_id:
					info = self.__dd_client.department.get(dd_dept_id_tmp)
					result.append(info.get('name', ''))
				return result
			if isinstance(dd_dept_id, int):
				info = self.__dd_client.department.get(dd_dept_id)
				return info.get('name', '')

	# 循环获取待确认到岗人员名单
	def __get_dd_user_pre_entry_list(self, user_list=[], offset=0, size=50):
		if offset == 0:
			user_list = []
		info = self.__dd_client.employeerm.querypreentry(offset, size=size)
		data_list = info['data_list']
		next_cursor = None
		try:
			next_cursor = info['next_cursor']
		except:
			pass
		data_list = data_list['string']
		user_list.extend(data_list)
		if next_cursor:
			offset += size
			return self.__get_dd_user_pre_entry_list(user_list=user_list, offset=offset, size=size)
		else:
			return user_list

	# 重置HR上关于钉钉的资料
	def __set_hr_del_dd_info(self, hr_user_code):
		__sql_str = r"update tps_empinfo set is_entry = 0, ischange_dd = 1, dd_id = null " \
					r"from tps_empinfo where empcode = '{user_code}' and isactive = 1"
		self.__hr_sql.sqlWork(__sql_str.format(user_code=hr_user_code))

	def __set_dd_new_info(self, hr_user_code):
		sqlStr1 = r"select top 1 a.is_entry,a.empname,a.staname,a.empcode,a.mobilephone,a.workplace,convert(varchar(20), " \
				  r"a.entrydate,120) as entrydate,b.dd_id as deptid,b.deptname  " \
				  r"from vps_empinfo a,torg_department b " \
				  r"where a.isactive = 1  " \
				  r"and isnull(is_entry,0) = 0  " \
				  r"and a.deptautoid=b.autoid  " \
				  r"and rtrim(isnull(a.mobilephone, '')) != ''  " \
				  r"and len(rtrim(a.mobilephone)) = 11 " \
				  r"and a.mobilephone like '[1][3456789]%' and a.mobilephone not like '%[^0-9]%' " \
				  r"and a.empcode = '{hr_user_code}'"

		sqlStr2 = r"update tps_empinfo set is_entry = 1, dd_id = '{dd_user_id}', ischange_dd = 1 " \
				  r"where empcode = '{hr_user_code}' "

		sql_info = self.__hr_sql.sqlWork(sqlStr1.format(hr_user_code=hr_user_code))
		if sql_info is not None:
			deptid = sql_info.at[0, 'deptid']
			deptname = sql_info.at[0, 'deptname']
			empcode = sql_info.at[0, 'empcode']
			empname = sql_info.at[0, 'empname']
			entrydate = sql_info.at[0, 'entrydate']
			position = sql_info.at[0, 'staname']
			mobile = sql_info.at[0, 'mobilephone']
			workplace = sql_info.at[0, 'workplace']

			extend_info = {'depts': deptid, 'mainDeptId': deptid, 'workPlace': workplace,
						   'position': position, 'jobNumber': empcode, 'employeeType': 1}
			info = self.__dd_client.employeerm.addpreentry(pre_entry_time=entrydate, name=empname,
													mobile=mobile, op_userid=self.__dd_op_user,
													extend_info=extend_info)
			dd_user_id = info['userid']
			errcode = info['errcode']
			if errcode == 0:
				self.__hr_sql.sqlWork(sqlStr2.format(dd_user_id=dd_user_id, hr_user_code=hr_user_code))
			status = True if errcode == 0 else False
			return status
		else:
			return False

	# 在钉钉上删除人员信息
	def __set_dd_del_info(self, dd_user_id):
		try:
			self.__dd_client.user.delete(dd_user_id)
		except Exception as e:
			print(str(e))
			pass

	def __set_dd_user_info_update(self, hr_user_code):
		sqlStr = r"SELECT empinfo.dd_id as userid, empinfo.empname as name,empinfo.empcode as jobnumber, empinfo.entrydate hireDate, " \
				 r"(case when empinfo_1.dd_id != empinfo.dd_id then empinfo_1.dd_id else '' end) as managerUserid, " \
				 r"isnull(empinfo.officeplace, '') as workPlace, department2.dept_dd_id as department, empinfo.staname as position " \
				 r"from vps_empinfo as empinfo " \
				 r"left join torg_station as station on station.autoid = empinfo.stationid " \
				 r"left join vorg_department as department on empinfo.deptid=department.deptid " \
				 r"left join vps_empinfo as empinfo_1 on empinfo_1.empcode=department.cus_partman " \
				 r"left join ( " \
				 r"	select emp_dd_id, dept_dd_id = " \
				 r"		(stuff((select ',' + dept1.dept_dd_id from " \
				 r"		(" \
				 r"			select empinfo.dd_id as emp_dd_id, department.dd_id as dept_dd_id from vps_empinfo as empinfo " \
				 r"			left join torg_department as department on empinfo.deptid = department.deptid " \
				 r"			where isactive = 1 " \
				 r"		) as dept1 where dept1.emp_dd_id = dept0.emp_dd_id for xml path('')),1,1,'')) " \
				 r"		from ( " \
				 r"			select empinfo.dd_id as emp_dd_id, department.dd_id as dept_dd_id from vps_empinfo as empinfo " \
				 r"			left join torg_department as department on empinfo.deptid = department.deptid " \
				 r"			where isactive = 1 " \
				 r"		) as dept0 " \
				 r"		group by emp_dd_id " \
				 r") as department2 on department2.emp_dd_id = empinfo.dd_id " \
				 r"where  empinfo.dd_id is not null and empinfo.is_entry = 1 " \
				 r"and empinfo.empcode = '{hr_user_code}' "
		sqlStr2 = r"UPDATE tps_empinfo SET ischange_dd = 0 WHERE empcode = '{hr_user_code}' "
		sql_data = self.__hr_sql.sqlWork(sqlStr.format(hr_user_code=hr_user_code))
		if sql_data is not None:
			update_info = {}
			update_info.update({'hireDate': int(datetime.datetime.timestamp(sql_data.at[0, 'hireDate']))*1000})
			update_info.update({'position': sql_data.at[0, 'position']})
			update_info.update({'jobnumber': sql_data.at[0, 'jobnumber']})
			update_info.update({'managerUserid': sql_data.at[0, 'managerUserid']})
			update_info.update({'department': [int(i) for i in sql_data.at[0, 'department'].split(',')]})
			update_info.update({'workPlace': sql_data.at[0, 'workPlace']})
			update_info.update({'userid': sql_data.at[0, 'userid']})
			update_info.update({'name': sql_data.at[0, 'name']})

			self.__dd_client.user.update(user_data=update_info)
			self.__hr_sql.sqlWork(sqlStr2.format(hr_user_code=hr_user_code))
