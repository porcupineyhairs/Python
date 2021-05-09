import dingtalk
from SqlHelper import MsSqlHelper
import datetime


app_key = "dingf8vlo9vvq0vqn84x"
app_secret = "PsAfaIWVe58ukgsvaBXHOxX0aW0LqUT5E54XmPDfXgzlL0srOVfnEDBIXBM4kLsg"
corp_id = "1045238247"

# 新 access_token 获取方式
client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)


def sql():
	sql = MsSqlHelper(host='comfort-hr.com', user='sa', passwd='WjzcomFort@2019', database='HYHRV3')

	sqlStr = r"SELECT empinfo.dd_id, empinfo.empcode,  empinfo.empname, empinfo.staname, empinfo.entrydate,  " \
	         r"empinfo_1.empcode,empinfo_1.empname, isnull(empinfo_1.dd_id, '') " \
	         r"from vps_empinfo as empinfo " \
	         r"left join torg_station as station on station.autoid = empinfo.stationid " \
	         r"left  join    vorg_department   as department  on  empinfo.deptid=department.deptid " \
	         r"left  join    vps_empinfo  as empinfo_1   on   empinfo_1.stacode  =department.stacode " \
	         r"where  empinfo.dd_id is not null and  empinfo.is_entry = 1 " \
	         r"and  empinfo.isactive = 1 and  empinfo.empcode like '0%' "
	# sqlStr += r" and empinfo.empcode = '002929' "

	get = sql.sqlWork(sqlStr)
	if get is not None:
		return get
	else:
		return None


def update():
	get = sql()
	if get is not None:
		for get_tmp in get:
			try:
				userid = get_tmp[0]
				u_jobnumber = get_tmp[1]
				u_position = get_tmp[3]
				u_hiredDate = int(datetime.datetime.timestamp(get_tmp[4]))*1000
				u_managerUserid = get_tmp[7]

				info = client.user.get(userid=userid)
				# print(info)


				o_jobnumber = info['jobnumber']
				o_position = info['position']
				o_hiredDate = info['hiredDate']
				try:
					o_managerUserid = info['managerUserid']
				except:
					o_managerUserid = ''
				# print(o_managerUserid)

				o_info = {'jobnumber': o_jobnumber, 'position': o_position, 'hiredDate': o_hiredDate,
				          'managerUserid': o_managerUserid}

				u_info = {'userid': userid, 'jobnumber': u_jobnumber, 'position': u_position, 'hiredDate': u_hiredDate, 'managerUserid': u_managerUserid}
				# print(u_info, o_info)

				if u_hiredDate != o_hiredDate or u_position != o_position or u_jobnumber != o_jobnumber or u_managerUserid != o_managerUserid:
					print(u_info, o_info)
					responce = client.user.update(user_data=u_info)
			except Exception as e:
				print('err', get_tmp[0], get_tmp[1], str(e))
				pass


def main():
	update()


if __name__ == '__main__':
	main()
