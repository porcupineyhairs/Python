from modules.SqlHelper import MsSqlHelper
from modules.LogHelper import logger
import datetime
import requests
import json


class DingTalk_Base:
	def __init__(self, url=''):
		self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
		self.url = url

	def send_msg(self, text, mobile=[""]):
		json_text = {
			"msgtype": "text",
			"text": {
				"content": text
			},
		}
		if mobile == 'all':
			json_text.update({"at": {
				"atMobiles": mobile,
				"isAtAll": True
			}})
		else:
			json_text.update({"at": {
				"atMobiles": mobile,
				"isAtAll": False
			}})
		
		return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content


class DingTalk_Disaster(DingTalk_Base):
	def __init__(self, url):
		super().__init__()
		# 填写机器人的url
		self.url = url


class WorkCardAlert:
	def __init__(self):
		self.sql = MsSqlHelper(host='comfort-hr.com', user='sa', passwd='WjzcomFort@2019', database='HYHRV3')

	# 消息发送的方法
	def onTimeAlarmSend(self, ding, textList=[], mobileList=[]):
		if len(textList) > 0:
			textSend = ''
			for text in textList:
				textSend += text + '\n'
			textSend.rstrip('\n')
			ding.send_msg(textSend, mobile=mobileList)

	# 获取人员信息
	def getEmpInfoDict(self, deptid):
		name_dict = {}
		sqlStr0 = r"select empname, empcode, mobilephone from vps_empinfo where deptid3 = '{deptid}' and isactive = 1"
		get_info = self.sql.sqlWork(sqlStr0.format(deptid=deptid))
		if get_info is not None:
			for index in range(get_info.shape[0]):
				empname = get_info.at[index, 'empname']
				empcode = get_info.at[index, 'empcode']
				empmobile = get_info.at[index, 'mobilephone']
				name_dict.update({empcode: {'name': empname, 'mobile': empmobile}})
		return name_dict

	# 获取人员假单信息
	def getKqLeave(self, deptid, empcode):
		sqlStr = r"select a.empcode,a.empname, isnull(b.leavetype+','+c.resttype ,'') leave from vps_empinfo a " \
				 r"left join (select empcode,empname,leavetype from vkq_leavereq where deptid3='{deptid}' and bd=CONVERT(VARCHAR,GETDATE(),23) GROUP BY empcode,empname,leavetype )b on a.empcode=b.empcode " \
				 r"left join (select  empcode,empname,resttype from vkq_restinput where deptid3='{deptid}' and yymmdd=CONVERT(VARCHAR,GETDATE(),23) GROUP BY empcode,empname,resttype )c on a.empcode=b.empcode " \
				 r"where a.deptid3='{deptid}' and a.isactive=1 and a.empcode='{empcode}' "
		get_leave = self.sql.sqlWork(sqlStr.format(deptid=deptid, empcode=empcode))
		if get_leave is not None:
			if get_leave.at[0, 'leave'] != '':
				return get_leave.at[0, 'leave']
			else:
				return None
		else:
			return None

	# 主执行方法
	def onTimeAlarmWork(self, deptid, url):
		ding = DingTalk_Disaster(url)
		now = datetime.datetime.now()
		hour = now.hour
		workTimeType = '上班' if hour < 12 else '下班'

		sqlStr1 = r"select  CONVERT(VARCHAR,GETDATE(),23)  as 打卡时间," \
				  r"a.empcode,a.empname,isnull(b.kqtime, '') as 早上打卡,isnull(c.kqtime, '') as 下午打卡 from vps_empinfo a " \
				  r"left join (select kqdate,empcode,empname,kqtime " \
				  r"from  vkq_attrecord where vkq_attrecord.kqdate=CONVERT(VARCHAR,GETDATE(),23) " \
				  r"and vkq_attrecord.deptid3='{deptid}' and left(kqtime,2)<=8 ) as b on a.empcode=b.empcode " \
				  r"left join (select kqdate,empcode,empname,kqtime " \
				  r"from  vkq_attrecord where vkq_attrecord.kqdate=CONVERT(VARCHAR,GETDATE(),23) " \
				  r"and vkq_attrecord.deptid3='{deptid}' and left(kqtime,2)>=17 ) c on a.empcode=c.empcode " \
				  r"where a.deptid3='{deptid}' and a.isactive='1'"

		# 获取人员信息
		name_dict = self.getEmpInfoDict(deptid=deptid)

		get_kq = self.sql.sqlWork(sqlStr1.format(deptid=deptid))
		if get_kq is not None:
			textList1 = []
			mobileList1 = []
			textList2 = []
			mobileList2 = []
			textList3 = []
			mobileList3 = []

			for index in range(get_kq.shape[0]):
				empcode = get_kq.at[index, 'empcode']
				onTime1 = get_kq.at[index, '早上打卡']
				onTime2 = get_kq.at[index, '下午打卡']
				# print(onTime1, onTime2)
				try:

					empcode_tmp = name_dict[empcode]
					empname = empcode_tmp['name']
					empmobile = empcode_tmp['mobile']

					timeTmp1 = onTime1.split(':')
					timeTmp2 = onTime2.split(':')

					# 清除有打卡记录的信息
					if empcode in name_dict.keys():
						del name_dict[empcode]

					if workTimeType == '上班':
						# 正常打卡
						if int(timeTmp1[0]) < 8:
							textList1.append(
								'{name}({empcode}){workTimeType}打卡时间为{time}'.format(name=empname, time=onTime1,
																					empcode=empcode,
																					workTimeType=workTimeType))
							mobileList1.append(empmobile)

						# 迟到
						elif int(timeTmp1[0]) >= 8 and int(timeTmp1[1]) > 0:
							textList2.append(
								'{name}({empcode})迟到，{workTimeType}打卡时间为{time}'.format(name=empname, time=onTime1,
																					   empcode=empcode,
																					   workTimeType=workTimeType))
							mobileList2.append(empmobile)
					else:
						# 正常打卡
						if int(timeTmp2[0]) >= 17 and onTime2 != '':
							textList1.append(
								'{name}({empcode}){workTimeType}打卡时间为{time}'.format(name=empname, time=onTime2,
																					empcode=empcode,
																					workTimeType=workTimeType))
							mobileList1.append(empmobile)

						# 早退
						elif int(timeTmp2[0]) < 17 and onTime2 != '':
							textList2.append(
								'{name}({empcode})早退，{workTimeType}打卡时间为{time}'.format(name=empname, time=onTime2,
																					   empcode=empcode,
																					   workTimeType=workTimeType))
							mobileList2.append(empmobile)

						else:
							textList2.append(
								'{name}({empcode}){workTimeType}缺卡'.format(name=empname, empcode=empcode,
																		   workTimeType=workTimeType))
							mobileList2.append(empmobile)
				except:
					pass

			# 缺勤
			if len(name_dict.keys()) > 0:
				for empcode in name_dict.keys():
					empcode_tmp = name_dict[empcode]
					empname = empcode_tmp['name']
					empmobile = empcode_tmp['mobile']

					kq_leave = self.getKqLeave(deptid=deptid, empcode=empcode)
					if kq_leave is not None:
						textList3.append(
							'{empname}({empcode}){workTimeType}请了{kqstr}'.format(empname=empname, empcode=empcode,
																				 kqstr=kq_leave,
																				 workTimeType=workTimeType))
						mobileList3.append(empmobile)
					else:
						textList3.append('{empname}({empcode}){workTimeType}缺勤'.format(empname=empname, empcode=empcode,
																					   workTimeType=workTimeType))
						mobileList3.append(empmobile)

			self.onTimeAlarmSend(ding, textList1, mobileList1)
			self.onTimeAlarmSend(ding, textList2, mobileList2)
			self.onTimeAlarmSend(ding, textList3, mobileList3)

	# 主入口
	def main(self):
		self.__init__()
		url_dict = {
			'0012911': 'https://oapi.dingtalk.com/robot/send?access_token=8530bcd5851c97058444c9215cf42580fc5ed399ae9b7742dd2c7541e27579da',
		}

		for deptid in url_dict.keys():
			url = url_dict[deptid]
			self.onTimeAlarmWork(deptid=deptid, url=url)
			logger.info('钉钉群 -- 发送刷卡记录')
		del self.sql
