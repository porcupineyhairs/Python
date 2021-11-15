import dingtalk
from SqlHelper import MsSqlHelper
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd


scheduler = BlockingScheduler()
sql = MsSqlHelper(host='comfort-hr.com', user='sa', passwd='WjzcomFort@2019', database='HYHRV3')

app_key = "dingf8vlo9vvq0vqn84x"
app_secret = "PsAfaIWVe58ukgsvaBXHOxX0aW0LqUT5E54XmPDfXgzlL0srOVfnEDBIXBM4kLsg"
corp_id = "1045238247"

# 新 access_token 获取方式
# client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)


# 更新员工信息
def user_update():
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	print('更新员工信息')

	sqlStr = r"SELECT empinfo.dd_id as dd_id, empinfo.empcode as jobnumber, empinfo.empname as name, " \
	         r"empinfo.staname as position, empinfo.entrydate hireDate,  " \
	         r"empinfo_1.empcode as managerUserJobnumber, empinfo_1.empname managerName, " \
	         r"(case when empinfo.dd_id = empinfo_1.dd_id then '' else isnull(empinfo_1.dd_id, '') end) managerUserid, " \
	         r"department.deptname as departmentName, department.dd_id as department, " \
	         r"isnull(empinfo.officeplace, '') as workPlace " \
	         r"from vps_empinfo as empinfo " \
	         r"left join torg_station as station on station.autoid = empinfo.stationid " \
	         r"left join vorg_department as department on empinfo.deptid=department.deptid " \
	         r"left join vps_empinfo as empinfo_1 on empinfo_1.empcode  =department.cus_partman " \
	         r"where empinfo.dd_id is not null and empinfo.is_entry = 1 " \
	         r"and empinfo.isactive = 1 "
	# sqlStr += r"and empinfo.topdeptid = '003' "
	sqlStr += r"and empinfo.ischange_dd = 1 "
	# sqlStr += r" and empinfo.empcode = '000037' "
	sqlStr += "order by empinfo.empcode "

	sql_get = sql.sqlWork(sqlStr)
	if sql_get is None:
		print('无需要更新的名单')
	else:
		print('开始更新人员信息')
		for index in range(len(sql_get)):
			dd_id = sql_get.at[index, 'dd_id']
			u_jobnumber = sql_get.at[index, 'jobnumber']
			u_name = sql_get.at[index, 'name']
			u_position = sql_get.at[index, 'position']
			# u_hiredDate = int(datetime.datetime.timestamp(get_tmp[4]))*1000
			u_managerUserid = sql_get.at[index, 'managerUserid']
			u_department = [int(sql_get.at[index, 'department'])]
			u_workPlace = sql_get.at[index, 'workPlace']

			try:

				info_user = client.user.get(userid=dd_id)
				print(info_user)

				try:
					o_jobnumber = info_user['jobnumber']
				except:
					o_jobnumber = ''
				try:
					o_name = info_user['name']
				except:
					o_name = ''
				try:
					o_position = info_user['position']
				except:
					o_position = ''
				# try:
				# 	o_hiredDate = info_user['hiredDate']
				# except:
				# 	o_hiredDate = ''
				try:
					o_managerUserid = info_user['managerUserid']
				except:
					o_managerUserid = ''
				try:
					o_department = info_user['department']
				except:
					o_department = []
				try:
					o_workPlace = info_user['workPlace']
				except:
					o_workPlace = ''

				old_info = {'name': o_name, 'jobnumber': o_jobnumber, 'position': o_position,
				          'managerUserid': o_managerUserid, 'department': o_department, 'workPlace': o_workPlace}

				# print(old_info)

				update_info = {}

				if u_position != o_position:
					update_info.update({'position': u_position})

				if u_jobnumber != o_jobnumber:
					update_info.update({'jobnumber': u_jobnumber})

				if u_managerUserid != o_managerUserid and u_managerUserid != '':
					update_info.update({'managerUserid': u_managerUserid})

				# if u_hiredDate != o_hiredDate:
				# 	update_info.update({'hiredDate': u_hiredDate})

				if u_name not in ['陈世宗']:
					if u_department != o_department:
						update_info.update({'department': u_department})

				if u_workPlace != o_workPlace:
					update_info.update({'workPlace': u_workPlace})

				if update_info != {}:
					# update_info.update({'userid': dd_id})
					print(update_info, old_info)

					try:
						responce = client.user.update(user_data=update_info)
						pass
					except Exception as e:
						print(str(e), u_jobnumber, u_name, update_info, old_info)

			except Exception as e:
				print(str(e), u_jobnumber, u_name, )


# 获取待入职名单_长度
def employeerm_querypreentry_len():
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	print('获取待入职名单')
	info = client.employeerm.querypreentry(offset=0, size=50)
	return len(info['data_list'])


# 获取待入职名单
def employeerm_querypreentry():
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	print('获取待入职名单')
	info = client.employeerm.querypreentry(offset=0, size=50)
	print(info)


# 删除离职员工
def user_delete():
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	print('删除离职员工')

	if False:
	# if employeerm_querypreentry_len() != 0:
		print('存在待入职名单，请先处理后再删除离职员工')

	else:
		print('开始删除离职员工')
		sqlStr1 = r"select dd_id, dd_id_bak, is_entry, empcode, empname from vps_empinfo where isactive = 0 " \
		          r"and isnull(dd_id, '') != '' order by empcode "

		sqlStr2 = r"update vps_empinfo set dd_id_bak = dd_id where isactive = 0 and empcode = '{0}' and dd_id = '{1}' "

		sqlStr3 = r"update vps_empinfo set dd_id = null, is_entry = 0 " \
		          r"where isactive = 0 and empcode = '{0}' and dd_id = '{1}'"

		get = sql.sqlWork(sqlStr1)
		if get is not None:
			for tmp in get:
				dd_id = tmp[0]
				empcode = tmp[3]
				empname = tmp[4]

				try:
					responce = client.user.delete(dd_id)

					errmsg = responce['errmsg']

					print(empcode, empname, dd_id, errmsg)

					if errmsg == 'ok':
						pass

				except Exception as e:
					print(empcode, empname, dd_id, str(e))

				finally:
					sql.sqlWork(sqlStr2.format(empcode, dd_id))
					sql.sqlWork(sqlStr3.format(empcode, dd_id))
		else:
			print('无需删除离职人员')


# 清除部门
def department_delete():
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	print('清除失效未同步的部门')
	# if employeerm_querypreentry_len() != 0:
	if False:
		print('存在待入职名单，请先处理后再清除失效未同步的部门')

	else:
		sqlStr0 = r"select dd_id, deptid, deptname from torg_department " \
		          r"where dd_id is not null " \
		          r"and isused = 0 " \
		          r"order by LEN(deptid) desc, deptid "

		sqlStr1 = r"update torg_department set dd_id = null where deptid = '{0}' and isused = 0 "

		sql_get = sql.sqlWork(sqlStr0)

		if sql_get is None:
			print('没有失效未同步的部门')
		else:
			print('开始清除失效未同步的部门')
			for index in range(len(sql_get)):
				dd_id = sql_get.at[index, 'dd_id']
				deptid = sql_get.at[index, 'deptid']
				deptname = sql_get.at[index, 'deptname']

				# dept_info = client.department.get(dd_id)

				try:
					client.department.delete(dd_id)
					sql.sqlWork(sqlStr1.format(deptid))
					print('已清除', deptid, deptname)
				except Exception as e:
					sql.sqlWork(sqlStr1.format(deptid))
					print(str(e), deptid, deptname, dd_id)


# 重置HR系统中已有钉钉信息，但未进入钉钉系统的人员标志位
def empinfo_reset():
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	sqlStr_get = r"SELECT empcode, is_entry, dd_id, dd_id_bak from vps_empinfo " \
			     r"where isactive = 1 and is_entry = 1 and isnull(dd_id, '') != '' " \
				 r"order by empcode "

	sqlStr_upd = r"update vps_empinfo set dd_id_bak = dd_id where empcode = '{0}' " \
				 r"update vps_empinfo set dd_id = null, is_entry = 0 where empcode = '{0}' "

	sql_get = sql.sqlWork(sqlStr_get)

	if sql_get is not None:
		for index in range(len(sql_get)):
			dd_id = sql_get.at[index, 'dd_id']
			empcode = sql_get.at[index, 'empcode']
			# print(dd_id, empcode)

			try:
				info_user = client.user.get(userid=dd_id)
				# print(info_user)
			except Exception as e:
				sql.sqlWork(sqlStr_upd.format(empcode))
				print(dd_id, empcode, 'update')


def main():
	user_delete()
	user_update()
	department_delete()
	# user_getDifferent()


if __name__ == '__main__':
	# empinfo_reset()
	# user_delete()
	user_update()
	# department_delete()

	# scheduler.add_job(trigger='interval', minutes=30, func=main)
	#
	# try:
	# 	scheduler.start()
	#
	# except (KeyboardInterrupt, SystemExit):
	# 	scheduler.shutdown()
	# 	print('Main_定时任务关闭')
	# except Exception as e:
	# 	print('Main:{}'.format(str(e)))
