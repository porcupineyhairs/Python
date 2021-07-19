from JdyHelper.JdyApi import APIUtils
from BaseHelper import MsSqlHelper
from Handler.Logger import Logger
import pandas as pd


# 报工记录日志明细表
api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
appId = '605d8c522ebb120009ba204a'
entryId = '60dab7d2fd77f40007771c6d'

# mssql_url = 'comfort-oa.com:60043'
mssql_url = '192.168.0.99'

api = APIUtils(appId, entryId, api_key)

log1 = Logger('-内销出货清单 -- 信息调整、生成报工日志')
log2 = Logger('-内销出货清单 -- 生成ERP单据')


def main_work():
	work1()
	work2()


# 信息调整
def work1():
	mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='COMFORT')
	sqlStrGet = r"SELECT 1 FROM COMFORT.dbo.COPTD WHERE RTRIM(TD001)+'-'+RTRIM(TD002)+'-'+RTRIM(TD003) = '{0}' "
	log1.log()
	# 按条件获取表单数据
	title = ['sell_type',
	         'remark', 'data_detail',
	         't_process_flag'
	         ]

	data_filter = {
		'rel': 'and',
		'cond': [
			api.set_dict_filter('t_process_flag', 'eq', '0')
		]
	}

	data = api.get_form_data('', 100, title, data_filter)

	if not data:
		log1.log('API返回无数据')
	else:
		log1.log('开始处理')
		for tmp in data:
			log1.log(tmp)
			_id = tmp['_id']
			data_detail = tmp['data_detail']
			remark = ''
			d_remark = ''
			t_process_flag = tmp['t_process_flag']

			update_detail = []

			try:
				err = 0
				for tmp2 in data_detail:
					d_remark = ''
					update_detail_tmp = {}
					d_index = tmp2['d_index']
					d_scan_id = tmp2['d_scan_id']
					d_process_flag_1 = tmp2['d_process_flag_1']

					# 构建原子单身的字典资料，真坑
					for key in tmp2.keys():
						api.set_dict_value(update_detail_tmp, key, tmp2[key])

					if d_process_flag_1 == '0':

						d_order_id = d_scan_id.split('/')[0]
						try:
							# ERP中是否存在订单
							df = mssql.sqlWork(sqlStrGet.format(d_order_id))
							print(df)
							if df is not None:
								d_process_flag_1 = 1
							else:
								d_remark = '序号{0}单号在ERP中不存在；'.format(d_index)
								err = 1
						except Exception as e:
							print(e)
							d_process_flag_1 = 1
							d_remark = d_remark + '序号{0}单号处理异常；'.format(d_index)
							err = 1
						finally:
							# api.set_dict_value(update_detail_tmp, '_id', _id2)
							api.set_dict_value(update_detail_tmp, 'd_order_id', d_order_id)
							api.set_dict_value(update_detail_tmp, 'd_process_flag_1', d_process_flag_1)
							update_detail.append(update_detail_tmp)
							remark += d_remark
					if err != 0:
						t_process_flag = '1-E'
					else:
						t_process_flag = '1'
			except:
				t_process_flag = '1-E'

			finally:
				update = {}
				api.set_dict_value(update, 'data_detail', update_detail)
				api.set_dict_value(update, 't_process_flag', t_process_flag)
				api.set_dict_value(update, 'remark', remark)
				# print(update)
				result = api.update_data(dataId=_id, data=update)


# 生成ERP单据
def work2():
	log2.log()
	# 按条件获取表单数据
	title = ['sell_type', 'erp_creator',
	         'remark', 'data_detail',
	         't_process_flag'
	         ]

	data_filter = {
		'rel': 'and',
		'cond': [
			api.set_dict_filter('t_process_flag', 'eq', '1')
		]
	}

	data = api.get_form_data('', 5, title, data_filter)

	if not data:
		log2.log('API返回无数据')
	else:
		log2.log('开始处理')
		for tmp in data:
			log2.log(tmp)
			_id = tmp['_id']
			creator = tmp['erp_creator']
			sell_type = tmp['sell_type'].split('.')[0]
			data_detail = tmp['data_detail']
			remark = ''
			t_process_flag = tmp['t_process_flag']

			update_detail = []
			dl = []

			try:
				for tmp2 in data_detail:
					update_detail_tmp = {}
					d_order_id = tmp2['d_order_id']
					d_num = tmp2['d_num']
					d_process_flag_2 = tmp2['d_process_flag_2']

					# 构建原子单身的字典资料，真坑
					for key in tmp2.keys():
						api.set_dict_value(update_detail_tmp, key, tmp2[key])

					update_detail.append(update_detail_tmp)

					dl.append([d_order_id, d_num])

				df = pd.DataFrame(data=dl, columns=['td', 'num'])
				df2 = df.groupby(df['td'], as_index=False).sum()

				coptg = Erp_Coptg(sellType=sell_type, creator=creator, df=df2)
				remark = '销货单号: ' + coptg.mainWork()

				t_process_flag = '2'
			except Exception as e:
				t_process_flag = '2-E'
				remark = str(e)
			finally:
				update = {}
				api.set_dict_value(update, 'data_detail', update_detail)
				api.set_dict_value(update, 't_process_flag', t_process_flag)
				api.set_dict_value(update, 'remark', remark)
				# print(update)
				result = api.update_data(dataId=_id, data=update)


class Erp_Coptg:
	def __init__(self, creator=None, sellType=None, df=None):
		self.mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='COMFORT')
		self.creator = creator
		self.tg001 = sellType
		self.df = df

		self.errFlag = False

		self.company = 'COMFORT'
		self.usr = None
		self.tg002 = None
		self.tg004 = []
		self.tg004Tmp = None
		self.tdList = []
		self.tdListStr = ''

		self.returnStr = ''

	def __del__(self):
		self.creator = None
		self.tg001 = None
		self.df = None

		self.usr = None
		self.tg002 = None
		self.tg004 = []
		self.tg004Tmp = None
		self.tdList = []
		self.tdListStr = ''

		self.returnStr = ''

	def mainWork(self):
		self.__init__(creator=self.creator, sellType=self.tg001, df=self.df)
		self.getUsrGroup()
		self.getTdList()
		self.getTdListStr()
		self.getTg004()

		for self.tg004Tmp in self.tg004:
			self.getTg002()
			self.insertHead()
			self.updateHead()
			self.insertDetail()
			self.updateDetail()
			self.updateHeadSeller()
			self.updateDetailMoney()
			self.updateHeadMoney()
			self.returnStr += self.tg001+'-'+self.tg002+'; '
		return self.returnStr

	def getUsrGroup(self):
		sqlStr = r"SELECT isnull(RTRIM(MF004), '') USR FROM dbo.ADMMF WHERE MF001 = '{0}' "
		df = self.mssql.sqlWork(sqlStr.format(self.creator))
		if df is not None:
			self.usr = df.at[0, 'USR']
		else:
			raise Exception('无法获取ERP账号')

	def getTg002(self):
		sqlStr = r"exec P_GETDH '{0}' "
		df = self.mssql.sqlWork(sqlStr.format(self.tg001))
		if df is not None:
			self.tg002 = df.at[0, 'DH']
		else:
			raise Exception('无法获取销货单号')

	def getTdList(self):
		try:
			if len(self.df):
				for index in range(len(self.df)):
					self.tdList.append(self.df.at[index, 'td'])
			else:
				raise Exception('传入订单明细为空')
		except:
			raise Exception('传入订单明细为空')

	def getTdListStr(self):
		for tmp in self.tdList:
			self.tdListStr += r"'" + tmp + r"',"
		self.tdListStr = self.tdListStr.rstrip(',')

	def getTg004(self):
		sqlStr = r"SELECT DISTINCT RTRIM(TC004) TC004 FROM COPTC " \
		         r"INNER JOIN COPTD ON TD001 = TC001 AND TD002 = TC002 " \
		         r"WHERE RTRIM(TD001)+'-'+RTRIM(TD002)+'-'+RTRIM(TD003) IN ({0}) "
		df = self.mssql.sqlWork(sqlStr.format(self.tdListStr))
		if df is not None:
			for index in range(len(df)):
				self.tg004.append(df.at[index, 'TC004'])
		else:
			raise Exception('无法获取客户编号')

	def insertHead(self):
		sqlStr = r"INSERT INTO COMFORT.dbo.COPTG (COMPANY, CREATOR, USR_GROUP, CREATE_DATE, FLAG, " \
		         r"TG001, TG002, TG003, TG042, UDF52) VALUES('{0}', '{1}', '{2}', dbo.f_getTime(1), 1, '{3}', '{4}', " \
		         r"LEFT(dbo.f_getTime(1), 8), LEFT(dbo.f_getTime(1), 8), 1) "
		self.mssql.sqlWork(sqlStr.format(self.company, self.creator, self.usr, self.tg001, self.tg002))

	def updateHead(self):
		sqlStr1 = r"UPDATE dbo.COPTG SET TG010 = '01', TG020 = '', TG022 = 0, TG023 = 'N', " \
		          r"TG024 = 'N', TG031 = 'N', TG036 = 'N', TG037 = 'N' " \
		          r"WHERE TG001 = '{0}' AND TG002 = '{1}' "

		sqlStr2 = r"UPDATE dbo.COPTG SET TG004 = MA001, TG005 = MA015, TG006 = MA016, TG008 = MA027, TG009 = MA064, " \
		          r"TG011 = MA014, TG012 = MG004, TG016 = MA037, TG017 = MA038, TG026 = MA085, TG044 = MA101, " \
		          r"TG047 = MA083, TG068 = MA113 " \
		          r"FROM( " \
		          r"    SELECT COPMAC. *, ISNULL(COPTGC.MG004, 0) AS MG004 " \
		          r"    FROM dbo.COPMA AS COPMAC LEFT JOIN( " \
		          r"        SELECT MA2.MA001, MA2.MA021, MG.MG002, MG.MG004 " \
		          r"        FROM dbo.COPMA AS MA2 LEFT JOIN dbo.CMSMG AS MG ON MG.MG001 = MA2.MA014 " \
		          r"        AND MG002 = (SELECT MAX(MG2.MG002) FROM CMSMG AS MG2 WHERE MG2.MG001 = MG.MG001 " \
		          r"        AND CONVERT(FLOAT, MG2.MG002) <= CONVERT(FLOAT, CONVERT(VARCHAR(8), GETDATE(), 112))) ) " \
		          r"    AS COPTGC ON COPTGC.MA001 = COPMAC.MA001 WHERE COPMAC.MA001 = '{2}' ) " \
		          r"AS COPMA WHERE TG001 = '{0}' AND TG002 = '{1}' "

		sqlStr3 = r"UPDATE dbo.COPTG SET TG044 =(CASE WHEN TG017 IN ('3','4','9') THEN 0 ELSE ISNULL(MA004, 0) END) " \
		          r"FROM dbo.COPTG LEFT JOIN dbo.CMSMA ON CMSMA.COMPANY = '{2}' WHERE TG001 = '{0}' AND TG002 = '{1}' "

		self.mssql.sqlWork(sqlStr1.format(self.tg001, self.tg002))
		self.mssql.sqlWork(sqlStr2.format(self.tg001, self.tg002, self.tg004Tmp))
		self.mssql.sqlWork(sqlStr3.format(self.tg001, self.tg002, self.company))

	def insertDetail(self):
		sqlStr = r"INSERT INTO dbo.COPTH (COMPANY, CREATOR, USR_GROUP, CREATE_DATE, FLAG, " \
		         r"TH001, TH002, TH003, TH008, TH014, TH015, TH016) " \
		         r"VALUES ('{0}', '{1}', '{2}', dbo.f_getTime(1), 1, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')"

		for index in range(len(self.df)):
			th003 = str(index+1).rjust(4, '0')
			num = self.df.at[index, 'num']
			td = self.df.at[index, 'td']
			th014, th015, th016 = td.split('-')
			self.mssql.sqlWork(sqlStr.format(self.company, self.creator, self.usr, self.tg001, self.tg002,
			                                 th003, num, th014, th015, th016))

	def updateDetail(self):
		sqlStr = r"UPDATE dbo.COPTH SET COPTH.CREATE_DATE = COPTG.CREATE_DATE, TH004 = TD004, TH005 = TD005, " \
		         r"TH006 = TD006, TH007 = TD007, TH009 = TD010, TH012 = TD011, TH017 = TH015, TH018 = TD020, " \
		         r"TH019 = TD014, TH020 = 'N', TH021 = 'N', TH025 = TD026, TH026 = 'N', TH031 = '1', TH048 = TD037, " \
		         r"TH049 = TD042, TH050 = TD043, TH055 = '', TH056 = '##########', TH063 = TD061, TH064 = TD062, " \
		         r"COPTH.UDF01 = COPTD.UDF01, COPTH.UDF03 = TQ003, COPTH.UDF04 = COPTD.UDF08, " \
		         r"COPTH.UDF05 = TD053, COPTH.UDF10 = COPTD.UDF10 " \
		         r"FROM dbo.COPTH AS COPTH " \
		         r"INNER JOIN dbo.COPTG ON TG001 = TH001 AND TG002 = TH002 " \
		         r"LEFT JOIN dbo.COPTD AS COPTD ON TH014 = TD001 AND TH015 = TD002 AND TH016 = TD003 " \
		         r"LEFT JOIN dbo.COPTQ AS COPTQ ON TQ001 = TD004 AND TQ002 = TD053 " \
		         r"WHERE 1=1 " \
		         r"AND TH001 = '{0}' AND TH002 = '{1}' "
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))

	def updateHeadSeller(self):
		sqlStr = r"UPDATE COPTG SET TG006 = TC006 " \
		         r"FROM COPTG " \
		         r"INNER JOIN COPTH ON TH001 = TG001 AND TH002 = TG002 " \
		         r"INNER JOIN COPTC ON TH014 = TC001 AND TH015 = TC002 " \
		         r"WHERE TG001 = '{0}' AND TG002 = '{1}'"
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))

	def updateDetailMoney(self):
		sqlStr = r"UPDATE dbo.COPTH SET TH013 = TH013C, TH035 = TH035C, TH036 = TH036C, TH037 = TH037C, TH038 = TH038C " \
		         r"FROM (SELECT TG001 AS TG001C, TG002 AS TG002C, TH003 AS TH003C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(TH008 * TH012 * TH025, 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN ROUND(TH008 * TH012 * TH025, 2) END) TH013C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN ROUND(TH008 * TH012 * TH025, 2) END) TH035C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(TH008 * TH012 * TH025, 2) - ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025 * TG044, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN 0 END) TH036C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2) * TG012, 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(ROUND(TH008 * TH012 * TH025, 2) * TG012, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN ROUND(TH008 * TH012 * TG012 * TH025, 2) END) TH037C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND((ROUND(TH008 * TH012 * TH025, 2) - ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2)) * TG012, 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025 * TG044 * TG012, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN 0 END) TH038C " \
		         r"FROM COPTH " \
		         r"INNER JOIN dbo.COPTG ON TG001 = TH001 AND TG002 = TH002 " \
		         r"WHERE TG001 = '{0}' AND TG002 = '{1}'" \
		         r") AS A0 " \
		         r"WHERE TH001 = TG001C AND TH002 = TG002C AND TH003 = TH003C "
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))

	def updateHeadMoney(self):
		sqlStr = r"UPDATE dbo.COPTG SET TG033 = TG033S, TG045 = TG045S, TG013 = TG013S, TG046 = TG046S, TG025 = TG025S " \
		         r"FROM (SELECT TH001, TH002, SUM(TH008) AS TG033S, SUM(TH037) AS TG045S, SUM(TH035) AS TG013S, " \
		         r"SUM(TH038) AS TG046S, SUM(TH036) AS TG025S FROM dbo.COPTH WHERE TH001 = '{0}' AND TH002 = '{1}' " \
		         r"GROUP BY TH001, TH002) AS A WHERE TG001 = TH001 AND TG002 = TH002"
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))


class Erp_Moctf:
	def __init__(self, creator=None, sellType=None, df=None):
		self.mssql = MsSqlHelper(host=mssql_url, user='sa', passwd='comfortgroup2016{', database='COMFORT')
		self.creator = creator
		self.tg001 = sellType
		self.df = df

		self.errFlag = False

		self.company = 'COMFORT'
		self.usr = None
		self.tg002 = None
		self.tg004 = []
		self.tg004Tmp = None
		self.tdList = []
		self.tdListStr = ''

		self.returnStr = ''

	def __del__(self):
		self.creator = None
		self.tg001 = None
		self.df = None

		self.usr = None
		self.tg002 = None
		self.tg004 = []
		self.tg004Tmp = None
		self.tdList = []
		self.tdListStr = ''

		self.returnStr = ''
		self.returnStr = ''

	def mainWork(self):
		self.__init__(creator=self.creator, sellType=self.tg001, df=self.df)
		self.getUsrGroup()
		self.getTdList()
		self.getTdListStr()
		self.getTg004()

		for self.tg004Tmp in self.tg004:
			self.getTg002()
			self.insertHead()
			self.updateHead()
			self.insertDetail()
			self.updateDetail()
			self.updateHeadSeller()
			self.updateDetailMoney()
			self.updateHeadMoney()
			self.returnStr += self.tg001+'-'+self.tg002+'; '
		return self.returnStr

	def getUsrGroup(self):
		sqlStr = r"SELECT isnull(RTRIM(MF004), '') USR FROM dbo.ADMMF WHERE MF001 = '{0}' "
		df = self.mssql.sqlWork(sqlStr.format(self.creator))
		if df is not None:
			self.usr = df.at[0, 'USR']
		else:
			raise Exception('无法获取ERP账号')

	def getTg002(self):
		sqlStr = r"exec P_GETDH '{0}' "
		df = self.mssql.sqlWork(sqlStr.format(self.tg001))
		if df is not None:
			self.tg002 = df.at[0, 'DH']
		else:
			raise Exception('无法获取销货单号')

	def getTdList(self):
		try:
			if len(self.df):
				for index in range(len(self.df)):
					self.tdList.append(self.df.at[index, 'td'])
			else:
				raise Exception('传入订单明细为空')
		except:
			raise Exception('传入订单明细为空')

	def getTdListStr(self):
		for tmp in self.tdList:
			self.tdListStr += r"'" + tmp + r"',"
		self.tdListStr = self.tdListStr.rstrip(',')

	def insertHead(self):
		sqlStr = r"INSERT INTO COMFORT.dbo.COPTG (COMPANY, CREATOR, USR_GROUP, CREATE_DATE, FLAG, " \
		         r"TG001, TG002, TG003, TG042, UDF52) VALUES('{0}', '{1}', '{2}', dbo.f_getTime(1), 1, '{3}', '{4}', " \
		         r"LEFT(dbo.f_getTime(1), 8), LEFT(dbo.f_getTime(1), 8), 1) "
		self.mssql.sqlWork(sqlStr.format(self.company, self.creator, self.usr, self.tg001, self.tg002))

	def updateHead(self):
		sqlStr1 = r"UPDATE dbo.COPTG SET TG010 = '01', TG020 = '', TG022 = 0, TG023 = 'N', " \
		          r"TG024 = 'N', TG031 = 'N', TG036 = 'N', TG037 = 'N' " \
		          r"WHERE TG001 = '{0}' AND TG002 = '{1}' "

		sqlStr2 = r"UPDATE dbo.COPTG SET TG004 = MA001, TG005 = MA015, TG006 = MA016, TG008 = MA027, TG009 = MA064, " \
		          r"TG011 = MA014, TG012 = MG004, TG016 = MA037, TG017 = MA038, TG026 = MA085, TG044 = MA101, " \
		          r"TG047 = MA083, TG068 = MA113 " \
		          r"FROM( " \
		          r"    SELECT COPMAC. *, ISNULL(COPTGC.MG004, 0) AS MG004 " \
		          r"    FROM dbo.COPMA AS COPMAC LEFT JOIN( " \
		          r"        SELECT MA2.MA001, MA2.MA021, MG.MG002, MG.MG004 " \
		          r"        FROM dbo.COPMA AS MA2 LEFT JOIN dbo.CMSMG AS MG ON MG.MG001 = MA2.MA014 " \
		          r"        AND MG002 = (SELECT MAX(MG2.MG002) FROM CMSMG AS MG2 WHERE MG2.MG001 = MG.MG001 " \
		          r"        AND CONVERT(FLOAT, MG2.MG002) <= CONVERT(FLOAT, CONVERT(VARCHAR(8), GETDATE(), 112))) ) " \
		          r"    AS COPTGC ON COPTGC.MA001 = COPMAC.MA001 WHERE COPMAC.MA001 = '{2}' ) " \
		          r"AS COPMA WHERE TG001 = '{0}' AND TG002 = '{1}' "

		sqlStr3 = r"UPDATE dbo.COPTG SET TG044 =(CASE WHEN TG017 IN ('3','4','9') THEN 0 ELSE ISNULL(MA004, 0) END) " \
		          r"FROM dbo.COPTG LEFT JOIN dbo.CMSMA ON CMSMA.COMPANY = '{2}' WHERE TG001 = '{0}' AND TG002 = '{1}' "

		self.mssql.sqlWork(sqlStr1.format(self.tg001, self.tg002))
		self.mssql.sqlWork(sqlStr2.format(self.tg001, self.tg002, self.tg004Tmp))
		self.mssql.sqlWork(sqlStr3.format(self.tg001, self.tg002, self.company))

	def insertDetail(self):
		sqlStr = r"INSERT INTO dbo.COPTH (COMPANY, CREATOR, USR_GROUP, CREATE_DATE, FLAG, " \
		         r"TH001, TH002, TH003, TH008, TH014, TH015, TH016) " \
		         r"VALUES ('{0}', '{1}', '{2}', dbo.f_getTime(1), 1, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')"

		for index in range(len(self.df)):
			th003 = str(index+1).rjust(4, '0')
			num = self.df.at[index, 'num']
			td = self.df.at[index, 'td']
			th014, th015, th016 = td.split('-')
			self.mssql.sqlWork(sqlStr.format(self.company, self.creator, self.usr, self.tg001, self.tg002,
			                                 th003, num, th014, th015, th016))

	def updateDetail(self):
		sqlStr = r"UPDATE dbo.COPTH SET COPTH.CREATE_DATE = COPTG.CREATE_DATE, TH004 = TD004, TH005 = TD005, " \
		         r"TH006 = TD006, TH007 = TD007, TH009 = TD010, TH012 = TD011, TH017 = TH015, TH018 = TD020, " \
		         r"TH019 = TD014, TH020 = 'N', TH021 = 'N', TH025 = TD026, TH026 = 'N', TH031 = '1', TH048 = TD037, " \
		         r"TH049 = TD042, TH050 = TD043, TH055 = '', TH056 = '##########', TH063 = TD061, TH064 = TD062, " \
		         r"COPTH.UDF01 = COPTD.UDF01, COPTH.UDF03 = TQ003, COPTH.UDF04 = COPTD.UDF08, " \
		         r"COPTH.UDF05 = TD053, COPTH.UDF10 = COPTD.UDF10 " \
		         r"FROM dbo.COPTH AS COPTH " \
		         r"INNER JOIN dbo.COPTG ON TG001 = TH001 AND TG002 = TH002 " \
		         r"LEFT JOIN dbo.COPTD AS COPTD ON TH014 = TD001 AND TH015 = TD002 AND TH016 = TD003 " \
		         r"LEFT JOIN dbo.COPTQ AS COPTQ ON TQ001 = TD004 AND TQ002 = TD053 " \
		         r"WHERE 1=1 " \
		         r"AND TH001 = '{0}' AND TH002 = '{1}' "
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))

	def updateHeadSeller(self):
		sqlStr = r"UPDATE COPTG SET TG006 = TC006 " \
		         r"FROM COPTG " \
		         r"INNER JOIN COPTH ON TH001 = TG001 AND TH002 = TG002 " \
		         r"INNER JOIN COPTC ON TH014 = TC001 AND TH015 = TC002 " \
		         r"WHERE TG001 = '{0}' AND TG002 = '{1}'"
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))

	def updateDetailMoney(self):
		sqlStr = r"UPDATE dbo.COPTH SET TH013 = TH013C, TH035 = TH035C, TH036 = TH036C, TH037 = TH037C, TH038 = TH038C " \
		         r"FROM (SELECT TG001 AS TG001C, TG002 AS TG002C, TH003 AS TH003C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(TH008 * TH012 * TH025, 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN ROUND(TH008 * TH012 * TH025, 2) END) TH013C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN ROUND(TH008 * TH012 * TH025, 2) END) TH035C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(TH008 * TH012 * TH025, 2) - ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025 * TG044, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN 0 END) TH036C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND(ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2) * TG012, 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(ROUND(TH008 * TH012 * TH025, 2) * TG012, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN ROUND(TH008 * TH012 * TG012 * TH025, 2) END) TH037C, " \
		         r"(CASE WHEN TG017 = '1' THEN ROUND((ROUND(TH008 * TH012 * TH025, 2) - ROUND(TH008 * TH012 * TH025 / (1 + TG044), 2)) * TG012, 2) " \
		         r"WHEN TG017 = '2' THEN ROUND(TH008 * TH012 * TH025 * TG044 * TG012, 2) " \
		         r"WHEN TG017 IN ('3', '4', '9') THEN 0 END) TH038C " \
		         r"FROM COPTH " \
		         r"INNER JOIN dbo.COPTG ON TG001 = TH001 AND TG002 = TH002 " \
		         r"WHERE TG001 = '{0}' AND TG002 = '{1}'" \
		         r") AS A0 " \
		         r"WHERE TH001 = TG001C AND TH002 = TG002C AND TH003 = TH003C "
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))

	def updateHeadMoney(self):
		sqlStr = r"UPDATE dbo.COPTG SET TG033 = TG033S, TG045 = TG045S, TG013 = TG013S, TG046 = TG046S, TG025 = TG025S " \
		         r"FROM (SELECT TH001, TH002, SUM(TH008) AS TG033S, SUM(TH037) AS TG045S, SUM(TH035) AS TG013S, " \
		         r"SUM(TH038) AS TG046S, SUM(TH036) AS TG025S FROM dbo.COPTH WHERE TH001 = '{0}' AND TH002 = '{1}' " \
		         r"GROUP BY TH001, TH002) AS A WHERE TG001 = TH001 AND TG002 = TH002"
		self.mssql.sqlWork(sqlStr.format(self.tg001, self.tg002))
