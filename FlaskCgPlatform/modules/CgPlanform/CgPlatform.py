from modules.Sql.MsSql import *
from modules.GlobalModules.DataConvert import *
from modules.GlobalModules.CheckSession import *
import json


class CgPlatform:
	def __init__(self):
		self.__sql198 = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		self.__sql99 = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')

	def getData(self, token, inDict):
		sqlStr99 = " exec P_Cg_Shl @sup_id='{0}', @sh_date='{1}' "
		sqlStr198 = "select wlno, sl from sh_detail where sh_date='{1}' and sup_id='{0}' order by sl "
		sqlStr198_2 = "select scaned_flag, sup_id+'-'+sh_date+idx from sh_title where sh_date='{1}' and sup_id='{0}'"

		rtnData = []
		rtnDict = {'success': 'no'}

		supId = CheckSession.getTokenValue(token=token, key='company_id')

		supDate = inDict['supDate'].replace('/', '').replace('-', '')

		getData99 = self.__sql99.sqlWork(sqlStr=sqlStr99.format(supId, supDate), getTitle=True)
		getData198 = self.__sql198.sqlWork(sqlStr=sqlStr198.format(supId, supDate))
		getData_scan = self.__sql198.sqlWork(sqlStr198_2.format(supId, supDate))
		scaned = getData_scan[0][0] if getData_scan is not None else False
		barCode = getData_scan[0][1] if getData_scan is not None else ''
		exist = True if getData_scan is not None else False

		if getData99 is not None:
			rtnData = getData99
			if getData198 is not None:
				for i in range(1, len(rtnData)):
					rtnData[i][5] = 0
				for tmp198 in getData198:
					for i in range(1, len(rtnData)):
						if rtnData[i][1] == tmp198[0]:
							rtnData[i][5] = tmp198[1]
							break

		data = list2Dict(rtnData) if rtnData is not None else None

		rtnDict.update({'success': 'yes', 'data': data, 'scaned': scaned, 'exist': exist, 'barCode': barCode})
		return rtnDict

	def setData(self, token, inDict):
		supId = CheckSession.getTokenValue(token=token, key='company_id')

		rtnDict = {'success': 'no'}

		supDate = inDict['supDate'].replace('/', '').replace('-', '')
		data = inDict['data']
		try:
			self.__uploadData(supId, supDate, data)
			rtnDict.update({'success': 'yes'})
		except Exception as e:
			rtnDict.update({'msg': '保存失败', 'err': str(e)})
		finally:
			return rtnDict

	def __uploadData(self, supId, supDate, data):
		sqlStrDelT = "delete from sh_title where sup_id='{0}' and sh_date='{1}'"
		sqlStrInsT = "insert into sh_title (create_date, sup_id, sh_date, idx) values(getdate(), '{0}', '{1}', '{2}') "
		sqlStrSltD = "select sup_id from sh_detail where sup_id='{0}' and sh_date='{1}'"
		sqlStrDelD = "delete from sh_detail where sup_id='{0}' and sh_date='{1}'"
		sqlStrInsD = "insert into sh_detail (sup_id, sh_date, xh, wlno, sl) values('{0}', '{1}', '{2}', '{3}', {4})"
		inDict = json.loads(data)
		self.__sql198.sqlWork(sqlStrDelT.format(supId, supDate))
		self.__sql198.sqlWork(sqlStrDelD.format(supId, supDate))
		for tmp in inDict:
			if float(tmp['送货量']) > 0:
				self.__sql198.sqlWork(sqlStrInsD.format(supId, supDate, tmp['序号'], tmp['品号'], float(tmp['送货量'])))
		if self.__sql198.sqlWork(sqlStrSltD.format(supId, supDate)) is not None:
			idx = CreateRandomCode.getRandomNum(lenth=4)
			self.__sql198.sqlWork(sqlStrInsT.format(supId, supDate, idx))
