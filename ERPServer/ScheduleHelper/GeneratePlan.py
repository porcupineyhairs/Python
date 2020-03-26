import sys
from datetime import datetime as dt
from SqlHelper.MsSql import MsSqlHelper
from BaseHelper.Log import Logger


class GeneratePlanException(Exception):
	def __init__(self, errInf):
		super().__init__(self)
		self.__errInf = errInf

	def __str__(self):
		return self.__errInf


class GeneratePlanHelper:
	def __init__(self, debug=False, logger=None, host=None):
		if logger is None:
			self.__logger = Logger(sys.path[0] + '/Log/GeneratePlan.log')
		else:
			self.__logger = logger
		self.__debugMode = debug
		if host is None:
			self.__host = '192.168.0.99'
		else:
			self.__host = host

		self.__mssql = None

		self.__scPlan = None
		self.__cgPlan = None
		self.__cpPlan = None

		self.workingFlag = False
		self.__situation1WorkingFlag = False
		self.__situation2WorkingFlag = False
		self.__situation3WorkingFlag = False
		self.__situation4WorkingFlag = False

	def __log(self, string, mode='info'):
		if mode == 'info':
			self.__logger.logger.info('GeneratePlan: {}'.format(string))
		elif mode == 'error':
			self.__logger.logger.error('GeneratePlan: {}'.format(string))
		elif mode == 'warning':
			self.__logger.logger.warning('GeneratePlan: {}'.format(string))

	def __del(self):
		del self.__mssql
		self.__mssql = None

		del self.__scPlan
		del self.__cgPlan
		del self.__cpPlan

		self.__scPlan = None
		self.__cgPlan = None
		self.__cpPlan = None

	def __clean(self):
		self.__situation1WorkingFlag = True
		self.__situation2WorkingFlag = True
		self.__situation3WorkingFlag = True
		self.__situation4WorkingFlag = True

		self.__scPlan = SCPlanHelper(logger=self.__logger, host=self.__host)
		self.__cgPlan = CGPlanHelper(logger=self.__logger, host=self.__host)
		self.__cpPlan = CPPlanHelper(logger=self.__logger, host=self.__host)

	def work(self):
		self.__log('Work Start')
		self.__clean()

		self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')

		self.workingFlag = True
		self.__situation1Work()
		self.__situation2Work()
		self.__situation3Work()
		self.__situation4Work()
		if not self.__situation1WorkingFlag and not self.__situation2WorkingFlag and \
				not self.__situation3WorkingFlag and not self.__situation4WorkingFlag:
			self.workingFlag = False

		self.__del()
		self.__log('Work Finished')

	# 没有跑过计划的订单
	def __situation1Work(self):
		__sqlStr = "SELECT TOP 1 RTRIM(TD.TD001)  AS TD001, RTRIM(TD.TD002) AS TD002, RTRIM(TD.TD003) AS TD003 " \
		           "FROM COMFORT.dbo.COPTD AS TD " \
		           "INNER JOIN COMFORT.dbo.INVMB ON TD004 = MB001 " \
		           "WHERE 1=1 " \
		           "AND EXISTS (" \
		           "	SELECT 1 FROM COMFORT.dbo.COPTD AS TD2 " \
		           "	INNER JOIN COMFORT.dbo.COPTC AS TC2 ON TC2.TC001 = TD.TD001 " \
		           "        AND TC2.TC002 = TD.TD002 AND TC2.TC027 = 'Y'" \
		           "	WHERE 1=1" \
		           "	AND TD.TD001 = TD2.TD001 AND TD.TD002 = TD2.TD002 AND TD.TD003 = TD2.TD003" \
		           "	AND TD2.TD016 = 'N' " \
		           "	AND TD2.UDF12 > '202003100000'" \
		           ") " \
		           "AND NOT EXISTS (" \
		           "	SELECT 1 FROM COMFORT.dbo.LRPLOG AS LG" \
		           "	WHERE 1=1" \
		           "	AND LG.TD001 = TD.TD001 AND LG.TD002 = TD.TD002 AND LG.TD003 = TD.TD003 " \
		           "	AND LG.PlanType = 'SC' " \
		           ") " \
		           "AND MB025 = 'M' " \
		           "AND TD.TD001 = '2215' " \
		           "ORDER BY TD.UDF12"

		while self.__situation1WorkingFlag:
			self.__situation1WorkingFlag = True
			__dataGet = self.__mssql.sqlWork(__sqlStr)
			if __dataGet is None:
				self.__situation1WorkingFlag = False
				self.__log('Situation1 Not Found Data!')
			else:
				self.__log('Situation1 Found Data:{}'.format(str(__dataGet[0])))
				__td001 = __dataGet[0][0]
				__td002 = __dataGet[0][1]
				__td003 = __dataGet[0][2]
				__planId = 'Auto' + str(__td001) + str(__td002) + str(__td003)
				self.__scPlan.work(td001=__td001, td002=__td002, td003=__td003, planId=__planId)
				self.__cgPlan.work(td001=__td001, td002=__td002, td003=__td003, planId=__planId)

	# 跑过计划且存在后期变更的订单
	def __situation2Work(self):
		__sqlStr = "SELECT TOP 1 RTRIM(TD.TD001)  AS TD001, RTRIM(TD.TD002) AS TD002, RTRIM(TD.TD003) AS TD003 " \
		           "FROM COMFORT.dbo.COPTD AS TD " \
		           "INNER JOIN COMFORT.dbo.INVMB ON TD004 = MB001 " \
		           "WHERE 1=1 " \
		           "AND EXISTS ( " \
		           "	SELECT 1 FROM COMFORT.dbo.COPTD AS TD2 " \
		           "	INNER JOIN COMFORT.dbo.COPTC AS TC2 ON TC2.TC001 = TD.TD001 AND TC2.TC002 = TD.TD002 " \
		           "        AND TC2.TC027 = 'Y' " \
		           "	WHERE 1=1 " \
		           "	AND TD.TD001 = TD2.TD001 AND TD.TD002 = TD2.TD002 AND TD.TD003 = TD2.TD003 " \
		           "	AND TD2.TD016 = 'N' " \
		           "	AND TD2.UDF12 > '202003100000' ) " \
		           "AND EXISTS ( " \
		           "	SELECT 1 FROM ( " \
		           "		SELECT TD001, TD002, TD003, MAX(PlanDate) AS PlanDate FROM COMFORT.dbo.LRPLOG " \
		           "		WHERE PlanType = 'SC' GROUP BY TD001, TD002, TD003 )AS LG " \
		           "	WHERE 1=1 " \
		           "	AND LG.TD001 = TD.TD001 AND LG.TD002 = TD.TD002 AND LG.TD003 = TD.TD003  " \
		           "	AND TD.UDF12 > LG.PlanDate ) " \
		           "AND MB025 = 'M' " \
		           "AND TD.TD001 = '2215' " \
		           "ORDER BY TD.UDF12 "
		__sqlStr2 = "SELECT MAX(TF003) FROM COMFORT.dbo.COPTF " \
		            "INNER JOIN COMFORT.dbo.COPTE ON TE001 = TF001 AND TF002 = TE002 " \
		            "WHERE 1=1 " \
		            "AND TE029 = 'Y' " \
		            "AND TF001 = '{tf001}' AND TF002 = '{tf002}' AND TF104 = '{tf003}'"

		while self.__situation2WorkingFlag:
			self.__situation2WorkingFlag = True
			__dataGet = self.__mssql.sqlWork(__sqlStr)
			if __dataGet is None:
				self.__log('Situation2 Not Found Data!')
				self.__situation2WorkingFlag = False
			else:
				self.__log('Situation2 Found Data:{}'.format(str(__dataGet[0])))
				__td001 = __dataGet[0][0]
				__td002 = __dataGet[0][1]
				__td003 = __dataGet[0][2]
				__dataGet2 = self.__mssql.sqlWork(__sqlStr2.format(tf001=__td001, tf002=__td002, tf003=__td003))
				if __dataGet2 is not None:
					__bgVer = __dataGet2[0][0]
					__planId = 'Auto' + str(__td001) + str(__td002) + str(__td003) + '-BgVer' + str(__bgVer)
					self.__scPlan.work(td001=__td001, td002=__td002, td003=__td003, planId=__planId)
					self.__cgPlan.work(td001=__td001, td002=__td002, td003=__td003, planId=__planId)
				else:
					self.__log('Situation2 Not Found BgVer! - {}'.format(__dataGet[0]), mode='warning')

	# 没跑过计划，但订单中存在采购件的订单
	def __situation3Work(self):
		__sqlStr = "SELECT TOP 1 RTRIM(TC.TC001) AS TC001, RTRIM(TC.TC002) AS TC002 " \
		           "FROM COMFORT.dbo.COPTC AS TC " \
		           "WHERE 1=1 " \
		           "AND EXISTS ( " \
		           "	SELECT 1 FROM COMFORT.dbo.COPTD AS TD2 " \
		           "	INNER JOIN COMFORT.dbo.COPTC AS TC2 ON TC2.TC001 = TD2.TD001 AND TC2.TC002 = TD2.TD002 " \
		           "        AND TC2.TC027 = 'Y' " \
		           "	INNER JOIN COMFORT.dbo.INVMB ON TD2.TD004 = MB001 " \
		           "	WHERE 1=1 " \
		           "	AND TC.TC001 = TD2.TD001 AND TC.TC002 = TD2.TD002 " \
		           "	AND TD2.TD016 = 'N' " \
		           "	AND MB025 = 'P' " \
		           "	AND TD2.UDF12 > '202003100000' " \
		           "	AND NOT EXISTS ( " \
		           "		SELECT 1 FROM COMFORT.dbo.LRPLOG AS LG " \
		           "		WHERE 1=1 " \
		           "		AND LG.TD001 = TD2.TD001 AND LG.TD002 = TD2.TD002 " \
		           "		AND LG.PlanType = 'CP' " \
		           "	) " \
		           ") " \
		           "AND TC.TC001 = '2215' " \
		           "ORDER BY TC.TC001, TC.TC002"

		while self.__situation3WorkingFlag:
			__dataGet = self.__mssql.sqlWork(__sqlStr)
			if __dataGet is None:
				self.__log('Situation3 Not Found Data!')
				self.__situation3WorkingFlag = False
			else:
				self.__log('Situation3 Found Data:{}'.format(str(__dataGet[0])))
				__td001 = __dataGet[0][0]
				__td002 = __dataGet[0][1]
				__planId = 'Auto' + str(__td001) + str(__td002) + '-CP'
				self.__cpPlan.work(td001=__td001, td002=__td002, planId=__planId)

	# 跑过计划，但订单中存在采购件的订单，且后期变更过
	def __situation4Work(self):
		__sqlStr = "SELECT TOP 1 RTRIM(TC.TC001) AS TC001, RTRIM(TC.TC002) AS TC002 " \
		           "FROM COMFORT.dbo.COPTC AS TC " \
		           "WHERE 1=1 " \
		           "AND EXISTS ( " \
		           "	SELECT 1 FROM COMFORT.dbo.COPTD AS TD2 " \
		           "	INNER JOIN COMFORT.dbo.COPTC AS TC2 ON TC2.TC001 = TD2.TD001 AND TC2.TC002 = TD2.TD002 " \
		           "        AND TC2.TC027 = 'Y' " \
		           "	INNER JOIN COMFORT.dbo.INVMB ON TD2.TD004 = MB001 " \
		           "	WHERE 1=1 " \
		           "	AND TC.TC001 = TD2.TD001 AND TC.TC002 = TD2.TD002 " \
		           "	AND TD2.TD016 = 'N' " \
		           "	AND MB025 = 'P' " \
		           "	AND TD2.UDF12 > '202003100000' " \
		           "	AND EXISTS ( " \
		           "		SELECT 1 FROM COMFORT.dbo.LRPLOG AS LG " \
		           "		WHERE 1=1 " \
		           "		AND LG.TD001 = TD2.TD001 AND LG.TD002 = TD2.TD002 " \
		           "		AND LG.PlanType = 'CP' " \
		           "		GROUP BY LG.TD001, LG.TD002 HAVING TD2.UDF12 > MAX(LG.PlanDate) " \
		           "	) " \
		           ") " \
		           "AND TC.TC001 = '2215' " \
		           "ORDER BY TC.TC001, TC.TC002"
		__sqlStr2 = "SELECT MAX(TF003) FROM COMFORT.dbo.COPTF " \
		            "INNER JOIN COMFORT.dbo.COPTE ON TE001 = TF001 AND TF002 = TE002  " \
		            "INNER JOIN COMFORT.dbo.INVMB ON TF005 = MB001 " \
		            "WHERE 1=1 " \
		            "AND TE029 = 'Y' " \
		            "AND MB025 = 'P' " \
		            "AND TF001 = '{tf001}' AND TF002 = '{tf002}'"

		while self.__situation4WorkingFlag:
			__dataGet = self.__mssql.sqlWork(__sqlStr)
			if __dataGet is None:
				self.__log('Situation4 Not Found Data!')
				self.__situation4WorkingFlag = False
			else:
				self.__log('Situation4 Found Data:{}'.format(str(__dataGet[0])))
				__td001 = __dataGet[0][0]
				__td002 = __dataGet[0][1]
				__dataGet2 = self.__mssql.sqlWork(__sqlStr2.format(tf001=__td001, tf002=__td002))
				if __dataGet2 is not None:
					__bgVer = __dataGet2[0][0]
					__planId = 'Auto' + str(__td001) + str(__td002) + '-CP' + '-BgVer' + str(__bgVer)
					self.__cpPlan.work(td001=__td001, td002=__td002, planId=__planId)
				else:
					self.__log('Situation4 Not Found BgVer! - {}'.format(__dataGet[0]), mode='warning')


class CGPlanHelper:
	def __init__(self, debug=False, logger=Logger(sys.path[0] + '/Log/GeneratePlan.log'), host='192.168.0.99'):
		self.__logger = logger
		self.__debugMode = debug
		self.__host = host

		self.__mssql = None
		self.__td001 = None
		self.__td002 = None
		self.__td003 = None
		self.__planId = None
		self.__planVersion = None

	def __prepare(self):
		self.__mssql = None
		self.__td001 = None
		self.__td002 = None
		self.__td003 = None
		self.__planId = None
		self.__planVersion = None

	def work(self, td001=None, td002=None, td003=None, planId=None, planVersion='0001'):
		self.__logger.logger.info('GeneratePlan: CG: Main Work Start: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

		self.__prepare()
		self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')

		self.__td001 = td001
		self.__td002 = td002
		self.__td003 = td003
		self.__planId = planId
		self.__planVersion = planVersion

		try:
			self.__cleanLaLbTc()  # 先清除需要写入表中的信息，以防数据值重复写入，导致报错
			self.__insertLaLb()  # 采购计划信息写入表LRPTA，LRPTB
			self.__insertTc()  # 物料明细写入表LRPTC
			# self.__updateTcPrice()  # 获取每个品号的单价。已在TC中加入单价资料获取
			self.__lockCgPlan()  # 锁定采购计划

			self.__insertLog()

		except Exception as e:
			self.__logger.logger.error('GeneratePlan: CG: {0}\n\tErr: {1}'.
			                           format(str(self.__planId) + '-' + str(self.__planVersion), str(e)))

		finally:
			self.__logger.logger.info('GeneratePlan: CG: Main Work Finished: {}'.
			                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __cleanLaLbTc(self):
		sqlStr1 = "DELETE FROM COMFORT.dbo.LRPLA WHERE LA001='{planId}' AND LA012='{planVersion}' AND LA005='2' "
		sqlStr2 = "DELETE FROM COMFORT.dbo.LRPLB WHERE LB001='{planId}' AND LB017='{planVersion}' AND LB009='2' "
		sqlStr3 = "DELETE FROM COMFORT.dbo.LRPTC WHERE TC001='{planId}' AND TC046='{planVersion}' AND TC024='2' "

		self.__mssql.sqlWork(sqlStr=sqlStr1.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStr2.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStr3.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CG: CleanLaLbTc: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertLaLb(self):
		sqlStrLa = "INSERT INTO COMFORT.dbo.LRPLA (LA001, LA002, LA003, LA004, LA005, LA012, LA013, LA014, " \
		           "COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
		           "VALUES('{planId}', '3', '', '01', '2', '{planVersion}', '1', SUBSTRING(dbo.f_getTime(1), 1, 8), " \
		           "'COMFORT', dbo.f_getTime(1), 'Robot', '', 1) "

		sqlStrLb = "INSERT INTO COMFORT.dbo.LRPLB (LB001, LB002, LB003, LB004, LB005, LB006, LB007, LB008, LB009, LB010, " \
		           "LB017, COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
		           "VALUES('{planId}', '', '', '', SUBSTRING(dbo.f_getTime(1), 1, 8), " \
		           "SUBSTRING(dbo.f_getTime(1), 9, 2) + ':' + SUBSTRING(dbo.f_getTime(1), 11, 2), 'Robot', '', '2', " \
		           "'3', '{planVersion}', 'COMFORT', dbo.f_getTime(1), 'Robot', '', 1) "

		self.__mssql.sqlWork(sqlStr=sqlStrLa.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CG: InsLa: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

		self.__mssql.sqlWork(sqlStr=sqlStrLb.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CG: InsLb: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertTc(self):
		sqlStrTc = "INSERT INTO COMFORT.dbo.LRPTC (TC001, TC002, TC003,  TC004, TC005, TC006, TC007, TC008, TC009, TC010, " \
		           "TC011, TC012, TC013, TC014, TC015, TC016, TC017, TC018, TC019, TC020, TC021, TC022, TC023, TC024, " \
		           "TC025, TC026, TC027, TC028, TC029, TC030, TC031, TC033, TC034, TC035, TC042, TC043, TC044, TC045, TCC01, " \
		           "TC046, TC047, TC048, COMPANY, CREATOR, CREATE_DATE) " \
		           " " \
		           "SELECT TC001, TC002, TC003, MB032 AS TC004, MB017 AS TC005, TC006, LEFT(dbo.f_getTime(1), 8) AS TC007, " \
		           "'N' AS TC008, MA021 AS TC009, ISNULL(Price.TM010, 0) AS TC010, MB148 AS TC011, TC006 AS TC012, " \
		           "0 AS TC013, 0 AS TC014, 0 AS TC015, 0 AS TC016, 0 AS TC017, 0 AS TC018, 0 AS TC019, 0 AS TC020, " \
		           "0 AS TC021, 0 AS TC022, '' AS TC023, '2' AS TC024, " \
		           "RIGHT('0000' + CONVERT(VARCHAR(4), ROW_NUMBER() Over (ORDER BY TC001, TC002, TC003)), 4) AS TC025, " \
		           "TA047 AS TC026, TA048 AS TC027, TA049 AS TC028, 0 AS TC029, '' AS TC030, '' AS TC031, MB149 AS TC033, " \
		           "TC006 AS TC034, TC006 AS TC034, '3' AS TC042, 0 AS TC043, 0 AS TC044, 0 AS TC045, '' AS TCC01, TC046, " \
		           "'N' AS TC047, TC006 AS TC048, 'COMFORT', 'Robot', dbo.f_getTime(1) " \
		           "FROM ( " \
		           "	SELECT TA001 AS TC001, TA050 AS TC046, RTRIM(TB005) AS TC002, CAST(SUM(TB007) AS FLOAT) AS TC006,  " \
		           "	CONVERT(VARCHAR(8), DATEADD(DAY, -1, CONVERT(DATE, TA007 ,112)), 112) AS TC003 " \
		           "	FROM ( " \
		           "		SELECT TA001, INVMB.MB026 MB026,TB005,TA007,TB007,TA023,TA024,TA025,TB013,TB014,TB011," \
		           "            ISNULL(TB020,0) TB020,INVMB.MB004 MB004, INVMB.MB017 MB017, INVMB.MB025 MB025, " \
		           "            INVMB.MB032 MB032, INVMB.MB036 MB036,  INVMB.MB037 MB037, INVMB.MB038 MB038, " \
		           "            INVMB.MB039 MB039, INVMB.MB040 MB040, INVMB.MB068 MB068, INVMB.MB076 MB076, " \
		           "    		INVMB.MB148 MB148, INVMB.MB149 MB149, TB024, TB025, INVMB.MB022 MB022, INVMB.MB443 MB443, " \
		           "            TA037, TB009, TBC01,TA046,TA047,TA048,TA049,TA050,TA051 ,B.MB036 MB036B, " \
		           "    		B.MB037 MB037B,B.MB038 MB038B,TB030,TA003,TA053,TA054,INVMB.MB455 MB455,TA056,TA057, " \
		           "            TA058,TA059,TB028  ,TB017 " \
		           "		FROM COMFORT.dbo.LRPTA LRPTA " \
		           "		INNER JOIN COMFORT.dbo.INVMB B ON B.MB001=TA002 " \
		           "		INNER JOIN COMFORT.dbo.LRPTB LRPTB ON TA001=TB001 AND TA050=TB029 AND TA028=TB013 " \
		           "		INNER JOIN COMFORT.dbo.INVMB INVMB ON TB005=INVMB.MB001 " \
		           "		WHERE TA051='N' AND TA001='{planId}' AND TA050='{planVersion}' AND INVMB.MB025='P' AND TA009='Y' " \
		           "        AND TB007>0  AND (TB009='1' OR TB009='2')  AND INVMB.MB034='L'" \
		           "	) AS A GROUP BY TA001, TA050, TB005, TA007 " \
		           ") AS B " \
		           "INNER JOIN COMFORT.dbo.LRPTA ON TA001 = TC001 " \
		           "INNER JOIN COMFORT.dbo.INVMB ON MB001 = TC002 " \
		           "INNER JOIN COMFORT.dbo.PURMA ON MA001 = MB032 " \
		           "LEFT JOIN V_GetPrice  AS Price ON Price.TM004 = TC002 AND Price.TL004 = MA001 " \
		           "WHERE 1=1 " \
		           "ORDER BY TC001, TC002, TC003"
		self.__mssql.sqlWork(sqlStr=sqlStrTc.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CG: InsTc: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __updateTcPrice(self):
		sqlStr = "SELECT TC002, TC004 FROM COMFORT.dbo.LRPTC WHERE TC001 = '{planId}' AND TC046 = '{planVersion}' "
		sqlStr2 = "UPDATE COMFORT.dbo.LRPTC SET TC010 = TM010 " \
		          "FROM COMFORT.dbo.LRPTC " \
		          "LEFT JOIN ( " \
		          "	SELECT TOP 1 TM004, TL004, TM010 FROM V_GetPrice " \
		          "	WHERE TM004 = '{tc002}' AND TL004 = '{tc004}' " \
		          "	ORDER BY TM014 DESC, TL003 DESC " \
		          ") AS K ON TM004 = TC002 AND TL004 = TC004 " \
		          "WHERE 1=1 " \
		          "AND TC001 = '{planId}' AND TC002 = '{tc002}' AND TC004 = '{tc004}' AND TC046 = '{planVersion}' "
		__getData = self.__mssql.sqlWork(sqlStr=sqlStr.format(planId=self.__planId, planVersion=self.__planVersion))

		for __getTmp in __getData:
			self.__mssql.sqlWork(sqlStr=sqlStr2.format(planId=self.__planId, planVersion=self.__planVersion,
			                                           tc002=str(__getTmp[0]), tc004=str(__getTmp[1])))

		self.__logger.logger.info('GeneratePlan: CG: UpdTcPrince: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __lockCgPlan(self):
		sqlStr = "UPDATE COMFORT.dbo.LRPTC SET ,TC008='Y', COMPANY='COMFORT', MODIFIER='Robot', " \
		         "MODI_DATE=dbo.f_getTime(1), FLAG=(convert(int,COMFORT.dbo.LRPTC.FLAG))%999+1  " \
		         "FROM COMFORT.dbo.LRPTC " \
		         "INNER JOIN COMFORT.dbo.LRPLA ON TC001=LA001 AND TC046 = LA012 " \
		         "LEFT  JOIN COMFORT.dbo.LRPLB ON LA001=LB001 AND LA005=LB009 AND LA012 = LB017 " \
		         "WHERE 1=1 " \
		         "AND LA005='2' AND LA013 <> '3' " \
		         "AND RTRIM(LA001) = '{planId}' " \
		         "AND RTRIM(LA012) = '{planVersion}' " \
		         "AND TC008='N' "
		self.__mssql.sqlWork(sqlStr.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CG: LockCgPlan: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertLog(self):
		if not self.__debugMode:
			sqlStr = "INSERT INTO COMFORT.dbo.LRPLOG (TD001, TD002, TD003, PlanID, PlanVersion, PlanType, PlanDate) " \
			         "VALUES('{td001}', '{td002}', '{td003}', '{planId}', '{planVersion}', 'CG', " \
			         "CONVERT(VARCHAR(12), dbo.f_getTime(1)))"
			self.__mssql.sqlWork(sqlStr=sqlStr.format(td001=self.__td001, td002=self.__td002, td003=self.__td003,
			                                          planId=self.__planId, planVersion='0001'))
			self.__logger.logger.info('GeneratePlan: CG: InsLrpLog: {}'.
			                          format(str(self.__planId) + '-' + str(self.__planVersion)))


class CPPlanHelper:
	def __init__(self, debug=False, logger=Logger(sys.path[0] + '/Log/GeneratePlan.log'), host='192.168.0.99'):
		self.__logger = logger
		self.__debugMode = debug
		self.__host = host

		self.__mssql = None
		self.__td001 = None
		self.__td002 = None
		self.__td003 = None
		self.__planId = None
		self.__planVersion = None

	def __prepare(self):
		self.__mssql = None
		self.__td001 = None
		self.__td002 = None
		self.__td003 = None
		self.__planId = None
		self.__planVersion = None

	def work(self, td001=None, td002=None, td003=None, planId=None, planVersion='0001'):
		self.__prepare()
		self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')

		self.__td001 = td001
		self.__td002 = td002
		self.__td003 = td003
		self.__planId = planId
		self.__planVersion = planVersion

		try:
			self.__insertLog()

		except Exception as e:
			self.__logger.logger.error('GeneratePlan: CP: {0}\n\tErr: {1}'.
			                           format(str(self.__planId) + '-' + str(self.__planVersion), str(e)))

		finally:
			self.__logger.logger.info('GeneratePlan: CP: Main Work Finished: {}'.
			                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertLaLb(self):
		sqlStrLa = "INSERT INTO COMFORT.dbo.LRPLA (LA001, LA002, LA003, LA004, LA005, LA012, LA013, LA014, " \
		           "COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
		           "VALUES('{planId}', '3', '', '01', '2', '{planVersion}', '1', SUBSTRING(dbo.f_getTime(1), 1, 8), " \
		           "'COMFORT', dbo.f_getTime(1), 'Robot', '', 1) "

		sqlStrLb = "INSERT INTO COMFORT.dbo.LRPLB (LB001, LB002, LB003, LB004, LB005, LB006, LB007, LB008, LB009, LB010, " \
		           "LB017, COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
		           "VALUES('{planId}', '', '', '', SUBSTRING(dbo.f_getTime(1), 1, 8), " \
		           "SUBSTRING(dbo.f_getTime(1), 9, 2) + ':' + SUBSTRING(dbo.f_getTime(1), 11, 2), 'Robot', '', '2', " \
		           "'3', '{planVersion}', 'COMFORT', dbo.f_getTime(1), 'Robot', '', 1) "

		self.__mssql.sqlWork(sqlStr=sqlStrLa.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStrLb.format(planId=self.__planId, planVersion=self.__planVersion))

	def __insertTc(self):
		sqlStrTc = "INSERT INTO COMFORT.dbo.LRPTC (TC001, TC002, TC003,  TC004, TC005, TC006, TC007, TC008, TC009, TC010, " \
		           "TC011, TC012, TC013, TC014, TC015, TC016, TC017, TC018, TC019, TC020, TC021, TC022, TC023, TC024, " \
		           "TC025, TC026, TC027, TC028, TC029, TC030, TC031, TC033, TC034, TC035, TC042, TC043, TC044, TC045, TCC01, " \
		           "TC046, TC047, TC048, COMPANY, CREATOR, CREATE_DATE) " \
		           " " \
		           "SELECT TC001, TC002, TC003, MB032 AS TC004, MB017 AS TC005, TC006, LEFT(dbo.f_getTime(1), 8) AS TC007, " \
		           "'N' AS TC008, MA021 AS TC009, 0 AS TC010, MB148 AS TC011, TC006 AS TC012, 0 AS TC013, 0 AS TC014, " \
		           "0 AS TC015, 0 AS TC016, 0 AS TC017, 0 AS TC018, 0 AS TC019, 0 AS TC020, 0 AS TC021, 0 AS TC022, " \
		           "'' AS TC023, '2' AS TC024, " \
		           "RIGHT('0000' + CONVERT(VARCHAR(4), ROW_NUMBER() Over (ORDER BY TC001, TC002, TC003)), 4) AS TC025, " \
		           "TA047 AS TC026, TA048 AS TC027, TA049 AS TC028, 0 AS TC029, '' AS TC030, '' AS TC031, MB149 AS TC033, " \
		           "TC006 AS TC034, TC006 AS TC034, '3' AS TC042, 0 AS TC043, 0 AS TC044, 0 AS TC045, '' AS TCC01, TC046, " \
		           "'N' AS TC047, TC006 AS TC048, 'COMFORT', 'Robot', dbo.f_getTime(1) " \
		           "FROM ( " \
		           "	SELECT TA001 AS TC001, TA050 AS TC046, RTRIM(TB005) AS TC002, CAST(SUM(TB007) AS FLOAT) AS TC006,  " \
		           "	CONVERT(VARCHAR(8), DATEADD(DAY, -1, CONVERT(DATE, TA007 ,112)), 112) AS TC003 " \
		           "	FROM ( " \
		           "		SELECT TA001, INVMB.MB026 MB026,TB005,TA007,TB007,TA023,TA024,TA025,TB013,TB014,TB011," \
		           "            ISNULL(TB020,0) TB020,INVMB.MB004 MB004, INVMB.MB017 MB017, INVMB.MB025 MB025, " \
		           "            INVMB.MB032 MB032, INVMB.MB036 MB036,  INVMB.MB037 MB037, INVMB.MB038 MB038, " \
		           "            INVMB.MB039 MB039, INVMB.MB040 MB040, INVMB.MB068 MB068, INVMB.MB076 MB076, " \
		           "    		INVMB.MB148 MB148, INVMB.MB149 MB149, TB024, TB025, INVMB.MB022 MB022, INVMB.MB443 MB443, " \
		           "            TA037, TB009, TBC01,TA046,TA047,TA048,TA049,TA050,TA051 ,B.MB036 MB036B, " \
		           "    		B.MB037 MB037B,B.MB038 MB038B,TB030,TA003,TA053,TA054,INVMB.MB455 MB455,TA056,TA057, " \
		           "            TA058,TA059,TB028  ,TB017 " \
		           "		FROM COMFORT.dbo.LRPTA LRPTA " \
		           "		INNER JOIN COMFORT.dbo.INVMB B ON B.MB001=TA002 " \
		           "		INNER JOIN COMFORT.dbo.LRPTB LRPTB ON TA001=TB001 AND TA050=TB029 AND TA028=TB013 " \
		           "		INNER JOIN COMFORT.dbo.INVMB INVMB ON TB005=INVMB.MB001 " \
		           "		WHERE TA051='N' AND TA001='{planId}' AND TA050='{planVersion}' AND INVMB.MB025='P' AND TA009='Y' " \
		           "        AND TB007>0  AND (TB009='1' OR TB009='2')  AND INVMB.MB034='L'" \
		           "	) AS A GROUP BY TA001, TA050, TB005, TA007 " \
		           ") AS B " \
		           "INNER JOIN COMFORT.dbo.LRPTA ON TA001 = TC001 " \
		           "INNER JOIN COMFORT.dbo.INVMB ON MB001 = TC002 " \
		           "INNER JOIN COMFORT.dbo.PURMA ON MA001 = MB032 " \
		           "WHERE 1=1 " \
		           "ORDER BY TC001, TC002, TC003"
		self.__mssql.sqlWork(sqlStr=sqlStrTc.format(planId=self.__planId, planVersion=self.__planVersion))

	def __lockCgPlan(self):
		sqlStr = "UPDATE COMFORT.dbo.LRPTC SET ,TC008='Y', COMPANY='COMFORT', MODIFIER='Robot', " \
		         "MODI_DATE=dbo.f_getTime(1), FLAG=(convert(int,COMFORT.dbo.LRPTC.FLAG))%999+1  " \
		         "FROM COMFORT.dbo.LRPTC " \
		         "INNER JOIN COMFORT.dbo.LRPLA ON TC001=LA001 AND TC046 = LA012 " \
		         "LEFT  JOIN COMFORT.dbo.LRPLB ON LA001=LB001 AND LA005=LB009 AND LA012 = LB017 " \
		         "WHERE 1=1 " \
		         "AND LA005='2' AND LA013 <> '3' " \
		         "AND RTRIM(LA001) = '{planId}' " \
		         "AND RTRIM(LA012) = '{planVersion}' " \
		         "AND TC008='N' "
		self.__mssql.sqlWork(sqlStr.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CP: LockCpPlan: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertLog(self):
		if not self.__debugMode:
			sqlStr = "INSERT INTO COMFORT.dbo.LRPLOG (TD001, TD002, TD003, PlanID, PlanVersion, PlanType, PlanDate) " \
			         "VALUES('{td001}', '{td002}', '{td003}', '{planId}', '{planVersion}', 'CP', " \
			         "CONVERT(VARCHAR(12), dbo.f_getTime(1)))"
			self.__mssql.sqlWork(sqlStr=sqlStr.format(td001=self.__td001, td002=self.__td002, td003=self.__td003,
			                                          planId=self.__planId, planVersion=self.__planVersion))
			self.__logger.logger.info('GeneratePlan: CP: InsLrpLog: {}'.
			                          format(str(self.__planId)) + '-' + str(self.__planVersion))


class SCPlanHelper:
	def __init__(self, debug=False, logger=Logger(sys.path[0] + '/Log/GeneratePlan.log'), host='192.168.0.99'):
		self.__logger = logger
		self.__debugMode = debug
		self.__host = host

		self.__mssql = None
		self.__td001 = None
		self.__td002 = None
		self.__td003 = None
		self.__dd = None
		self.__planId = None
		self.__planVersion = None

		self.__timeStr = None
		self.__ph = None
		self.__pz = None
		self.__sl = None

	def __prepare(self):
		self.__mssql = None
		self.__td001 = None
		self.__td002 = None
		self.__td003 = None
		self.__dd = None
		self.__planId = None
		self.__planVersion = None

		self.__timeStr = None
		self.__ph = None
		self.__pz = None
		self.__sl = None

	def work(self, td001=None, td002=None, td003=None, planId=None, planVersion='0001'):
		self.__prepare()
		self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')

		self.__td001 = td001
		self.__td002 = td002
		self.__td003 = td003
		self.__dd = self.__td001 + '-' + self.__td002 + '-' + self.__td003
		self.__planId = planId
		self.__planVersion = planVersion

		try:
			self.__insertLog()

		except Exception as e:
			self.__logger.logger.error('GeneratePlan: SC: {0}\n\tErr: {1}'.
			                           format(str(self.__planId) + '-' + str(self.__planVersion), str(e)))

		finally:
			self.__logger.logger.info('GeneratePlan: SC: Main Work Finished: {}'.
			                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __lockScPlan(self):
		sqlStr = "UPDATE COMFORT.dbo.LRPTA SET TA009='Y', COMPANY='COMFORT', MODIFIER='Robot', " \
		         "MODI_DATE=dbo.f_getTime(1), FLAG=(CONVERT ( INT, COMFORT.dbo.LRPTA.FLAG )) % 999+1  " \
		         "FROM COMFORT.dbo.LRPTA " \
		         "INNER JOIN COMFORT.dbo.LRPLA ON TA001 = LA001 AND LA012 = TA050 " \
		         "LEFT JOIN COMFORT.dbo.LRPLB ON LA001 = LB001 AND LA005 = LB009 AND LA012 = LB017 " \
		         "WHERE 1=1 " \
		         "AND LA005 = '1' AND LA013 <> '3' " \
		         "AND RTRIM(LA001) = '{planId}' " \
		         "AND RTRIM(LA012) = '{planVersion}' " \
		         "AND TA009 = 'N' "
		self.__mssql.sqlWork(sqlStr.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: CG: LockCgPlan: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertLog(self):
		if not self.__debugMode:
			sqlStr = "INSERT INTO COMFORT.dbo.LRPLOG (TD001, TD002, TD003, PlanID, PlanVersion, PlanType, PlanDate) " \
			         "VALUES('{td001}', '{td002}', '{td003}', '{planId}', '{planVersion}', 'SC', " \
			         "CONVERT(VARCHAR(12), dbo.f_getTime(1)))"
			self.__mssql.sqlWork(sqlStr=sqlStr.format(td001=self.__td001, td002=self.__td002, td003=self.__td003,
			                                          planId=self.__planId, planVersion='0001'))
			self.__logger.logger.info('GeneratePlan: SC: InsLrpLog: {}'.
			                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __getTimeStr(self):
		self.__timeStr = self.__mssql.sqlWork("SELECT RIGHT(COMFORT.dbo.f_getTime(1), 8) AS T")[0][0]

	def __getOrder(self):
		sqlStr = "SELECT TD004, CAST(TD008-TD009 AS FLOAT), TD053 FROM COMFORT.dbo.COPTD " \
		         "WHERE TD001='{td001}' AND TD002='{td002}' AND TD003='{td003}'"
		__getData = self.__mssql.sqlWork(sqlStr.format(td001=self.__td001, td002=self.__td002, td003=self.__td003))
		if __getData is not None:
			self.__ph = __getData[0][0]
			self.__sl = __getData[0][1]
			self.__pz = __getData[0][2]

	def __cleanLaLbTaTbTe(self):
		sqlStr1 = "DELETE FROM COMFORT.dbo.LRPLA WHERE LA001='{planId}' AND LA012='{planVersion}' AND LA005='1' "
		sqlStr2 = "DELETE FROM COMFORT.dbo.LRPLB WHERE LB001='{planId}' AND LB017='{planVersion}' AND LB009='1' "
		sqlStr3 = "DELETE FROM COMFORT.dbo.LRPTA WHERE TA001='{planId}' AND TA050='{planVersion}' AND TA026='1' "
		sqlStr4 = "DELETE FROM COMFORT.dbo.LRPTB WHERE TB001='{planId}' AND TB029='{planVersion}' AND TB012='1' "
		sqlStr5 = "DELETE FROM COMFORT.dbo.LRPTC WHERE TC001='{planId}' AND TC050='{planVersion}' AND TE005='1' "

		self.__mssql.sqlWork(sqlStr=sqlStr1.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStr2.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStr3.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStr4.format(planId=self.__planId, planVersion=self.__planVersion))
		self.__mssql.sqlWork(sqlStr=sqlStr5.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: SC: CleanLaLbTaTbTe: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __insertLaLb(self):
		sqlStrLa = "INSERT INTO COMFORT.dbo.LRPLA (LA001, LA002, LA003, LA004, LA005, LA012, LA013, LA014, " \
		           "COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
		           "VALUES('{planId}', '1', '', '01', '1', '{planVersion}', '1', SUBSTRING(dbo.f_getTime(1), 1, 8), " \
		           "'COMFORT', dbo.f_getTime(1), 'Robot', '', 1) "

		sqlStrLb = "INSERT INTO COMFORT.dbo.LRPLB (LB001, LB002, LB003, LB004, LB005, LB006, LB007, LB008, LB009, LB010, " \
		           "LB017, COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
		           "VALUES('{planId}', '{td001}', '{td002}', '{td003}', SUBSTRING(dbo.f_getTime(1), 1, 8), " \
		           "SUBSTRING(dbo.f_getTime(1), 9, 2) + ':' + SUBSTRING(dbo.f_getTime(1), 11, 2), 'Robot', '', '1', " \
		           "'1', '{planVersion}', 'COMFORT', dbo.f_getTime(1), 'Robot', '', 1) "

		self.__mssql.sqlWork(sqlStr=sqlStrLa.format(planId=self.__planId, planVersion=self.__planVersion))

		self.__logger.logger.info('GeneratePlan: SC: InsLa: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

		self.__mssql.sqlWork(sqlStr=sqlStrLb.format(planId=self.__planId, planVersion=self.__planVersion,
		                                            td001=self.__td001, td002=self.__td002, td003=self.__td003))

		self.__logger.logger.info('GeneratePlan: SC: InsLb: {}'.
		                          format(str(self.__planId) + '-' + str(self.__planVersion)))

	def __work(self):
		# 创建临时表LRPTEMP
		self.__mssql.sqlWork(("CREATE TABLE LRPWORK.dbo.LRPTEMP{timeStr} (LRPKEY numeric(7), LRP01 CHAR(02), "
		                     + "LRP02 CHAR(20), LRP03 CHAR(8), LRP04 numeric(16,6), LRP05 CHAR(4), LRP06 CHAR(11), "
		                     + "LRP07 CHAR(4), LRP08 CHAR(20), LRP09 CHAR(20), LRP10 CHAR(20), LRP11 CHAR(1) NULL, "
		                     + "MB004 CHAR(4), MB017 CHAR(20), MB025 CHAR(1), MB032 CHAR(10), MB036 numeric(16,6), "
		                     + "MB037 numeric(16,6), MB038 numeric(16,6), MB039 numeric(16,6), MB040 numeric(16,6), "
		                     + "MB041 numeric(16,6), MB068 CHAR(10), MB076 numeric(3), MB148 CHAR(4), MB149 CHAR(4), "
		                     + "LRP12 CHAR(40), LRP13 CHAR(4), LRP14 CHAR(1), LRP15 CHAR(1), LRP16 numeric(16,6), "
		                     + "LRP17 CHAR(20), LRP18 numeric(15,6), LRP19 CHAR(1), LRP20 CHAR(1), LRP21 numeric(16,6), "
		                     + "LRP22 CHAR(1), LRP23 CHAR(100), LRP24 CHAR(4), LRP25 CHAR(11), LRP26 CHAR(4), "
		                     + "LRP27 CHAR(8), LRP28 CHAR(8), LRP29 CHAR(4), LRP30 CHAR(1), LRP31 CHAR(1), "
		                     + "LRP32 numeric(16,6) NULL, LRP33 numeric(16,6) NULL, MB455 CHAR(1), "
		                     + "LRP34 numeric(16,6) NULL, LRP35 numeric(16,6) NULL, LRP36 CHAR(8), LRP37 CHAR(1), "
		                     + "PRIMARY KEY(LRPKEY))").format(self.__timeStr))

		# 获取品号信息并写入LRPTEMP
		self.__mssql.sqlWork(("INSERT INTO LRPWORK.dbo.LRPTEMP{timeStr} (LRPKEY,LRP01,LRP02,LRP03,LRP04,"
		                      "LRP05,LRP06,LRP07,LRP08,LRP09,LRP10,LRP11, MB017, MB025, MB032, MB036, "
		                      "MB037, MB038, MB039, MB040, MB068, MB076,MB004, MB148, MB149, LRP12, LRP13, "
		                      "LRP14, LRP15 , LRP16,LRP17,LRP18,LRP19, LRP20, LRP21, LRP22,LRP23,LRP24, "
		                      "LRP25,LRP26,LRP27,LRP28,LRP29,LRP30,LRP31,LRP32,LRP33,MB455,LRP34,LRP35, "
		                      "LRP36,LRP37) "
		                      "SELECT 1, MB026, RTRIM(TD004), TD013, QTY, TD001, RTRIM(TD002), TD003, '', "
		                      "'', '', 'N', MB017, MB025, MB032, MB036, MB037, MB038, MB039, MB040, MB068, "
		                      "MB076, TD010, MB148, MB149, TD053, '', MB022, MB443, 0, RTRIM(TD004), 0, "
		                      "MB455, '', 0, 'N', '00001', TD001, RTRIM(TD002), TD003, '', '', "
		                      "'{planVersion}', 'N', "
		                      "'0', 0, 0, 'N', 0, 0, TD013, 'Y' "
		                      "FROM ("
		                      "SELECT TD001,TD002,TD003,TD004,TD010,TD013,"
		                      "TD008+TD024-TD009-TD025-TD058 AS QTY ,MB026,MB004, MB017, MB025, MB032, "
		                      "MB036, MB037, MB038, MB039,MB040,MB068,MB076,MB148,MB149,MD003,MD004, "
		                      "TD053, MB022, MB443 ,MB455 "
		                      "FROM COMFORT.dbo.COPTD COPTD "
		                      "INNER JOIN COMFORT.dbo.INVMB INVMB ON TD004=MB001 "
		                      "INNER JOIN COMFORT.dbo.CMSMC CMSMC ON MC001=TD007 "
		                      "LEFT JOIN COMFORT.dbo.INVMD AS INVMD ON MD001 = TD004 AND MD002 = TD010 "
		                      "WHERE TD016='N' AND TD008+TD024-TD009-TD025-TD058>0 AND MC005='Y' "
		                      "AND ( TD001+'-'+RTRIM(TD002)+'-'+TD003='{dd}' ) AND MB034='L' "
		                      "AND MB025 IN ('M','S') "
		                      "AND NOT EXISTS (SELECT TA023 FROM COMFORT.dbo.LRPTA "
		                      "WHERE TD001=TA023 AND TD002=TA024 AND TD003=TA025 AND TA050='0001')"
		                      ") AS A").format(dd=self.__dd, timeStr=self.__timeStr,
		                                       planVersion=self.__planVersion))

		# 创建表BOMTEMP
		self.__mssql.sqlWork(("CREATE TABLE LRPWORK.dbo.BOMTEMP{timestr} (LEVEL char(2),BOM01 char(20), BOM02 char(20), "
		                      "BOM03 numeric(15,6), BOM04 numeric(15,6), BOM05 char(8), BOM06 char(8), "
		                      "BOM07 numeric(3,0), BOM08 char(1), BOM09 char(1), MB438 numeric(16,6), MB042 char(1), "
		                      "MB041 numeric(16,6), MB017 char(10), MD009 char(4), MB443 char(1), MD017 char(1), "
		                      "MB026 char(2), MB032 char(10), MB036 numeric(16,6), MB037 numeric(16,6), "
		                      "MB038 numeric(16,6), MB039 numeric(16,6), MB040 numeric(16,6), MB068 char(10), "
		                      "MB076 numeric(3,0), MB004 char(4), MB148 char(4), MB149 char(4), MB022 char(1), "
		                      "Root char(20), BOM10 CHAR(01), BOM11 CHAR(1))").format(timeStr=self.__timeStr))
