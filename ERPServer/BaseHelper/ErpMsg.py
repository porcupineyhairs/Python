from SqlHelper.MsSql import MsSqlHelper


class MsgHelperException(Exception):
	def __init__(self, errInf):
		super().__init__(self)
		self.__errInf = errInf

	def __str__(self):
		return self.__errInf


class MsgHelper:
	def __init__(self, debug=False):
		self.__debugMode = debug

		self.__company = ''
		self.__creator = None
		self.__title = ''
		self.__receivers = None
		self.__msgText = None

		self.__receiverStr = None
		self.__msgTextStr = None
		self.__msgId = None

		self.__mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='DSCSYS')

	def __doc__(self):
		pass

	# 邮件发送的主程序
	def sendMsg(self, company='COMFORT', creator=None, title='', sortMsg='', receivers=None, msgText=None):
		self.__company = company
		self.__creator = creator
		self.__title = title
		self.__sortMsg = sortMsg
		self.__receivers = receivers
		self.__msgText = msgText

		self.__checkCreator()
		self.__checkReceiver()
		self.__checkMsgText()

		self.__clean()

		self.__sendWork()

	def __clean(self):
		self.__receiverStr = None
		self.__msgTextStr = None
		self.__msgId = None

	# 检查接收人list是否有异常
	def __checkReceiver(self):
		if str(type(self.__receivers)) != r"<class 'list'>":
			raise MsgHelperException('Type of receivers is not a list! Please check!')

	def __checkMsgText(self):
		if str(type(self.__msgText)) != r"<class 'str'>":
			raise MsgHelperException('Type of msg_text is not a string! Please check!')

	def __checkCreator(self):
		if str(type(self.__creator)) != r"<class 'str'>":
			raise MsgHelperException('Type of creator is not a string! Please check!')

	def __checkSortMsg(self):
		if self.__sortMsg == '':
			self.__sortMsg = self.__title

	def __sendWork(self):
		self.__checkReceiver()
		self.__checkMsgText()
		self.__checkSortMsg()

		self.__setReceiverStr()
		self.__setMsgTextStr()
		self.__getMsgId()
		self.__setSql()

	def __setReceiverStr(self):
		self.__receiverStr = ""
		if self.__receivers is not None and len(self.__receivers) != 0:
			for rowIndex in range(len(self.__receivers)):
				self.__receiverStr += ("<R" + str(rowIndex + 1) + " ID=\"" + self.__receivers[rowIndex][0] + "\" Name=\""
				                       + self.__receivers[rowIndex][1] + "\" Type=\"1\" Msg=\"YNN\"/>")

	def __setMsgTextStr(self):
		self.__msgTextStr = '<FONT size=2>' + self.__msgText + '</FONT>'

	def __getMsgId(self):
		sqlStr = r"EXEC DSCSYS.dbo.P_GET_MSG_ID "
		sqlGet = self.__mssql.sqlWork(sqlStr)
		if sqlGet is not None:
			self.__msgId = sqlGet[0][0]

	def __setSql(self):
		sqlStr = "INSERT INTO DSCSYS.dbo.ADMTC ([COMPANY], [CREATOR], [USR_GROUP], [CREATE_DATE], [MODIFIER], " \
		         "[MODI_DATE], [FLAG], [TC001], [TC002], [TC003], [TC004], [TC005], [TC006], [TC007], [TC008], " \
		         "[TC009], [TC010], [TC011], [TC012], [TC013], [TC014], [TC015], [TC016], [TC017], [UDF01], [UDF02], " \
		         "[UDF03], [UDF04], [UDF05], [UDF06], [UDF51], [UDF52], [UDF53], [UDF54], [UDF55], [UDF56], [UDF07], " \
		         "[UDF08], [UDF09], [UDF10], [UDF11], [UDF12], [UDF57], [UDF58], [UDF59], [UDF60], [UDF61], [UDF62]) " \
		         "VALUES ('{company}', '{creator}', '', " \
		         "REPLACE(REPLACE(REPLACE(REPLACE(CONVERT(varchar(100), GETDATE(), 25), '-', ''), ' ', ''), ':', ''), " \
		         "'.', ''), " \
		         "NULL, NULL, 0, " \
		         "'{msgId}', '{creator}', '<?xml version=\"1.0\" encoding=\"GB2312\"?><Root>{receiverStr}</Root>', " \
		         "REPLACE(REPLACE(REPLACE(REPLACE(CONVERT(varchar(100), GETDATE(), 25), '-', ''), ' ', ''), ':', ''), " \
		         "'.', ''), " \
		         "'N', '{title}', '{sortMsg}', " \
		         "'<FONT size=2>{msgTextStr}</FONT>', " \
		         "'0', '', '', NULL, 0.000000, 0.000000, 0.000000, " \
		         "'<?xml version=\"1.0\" encoding=\"GB2312\"?><Root><Dispatching Enable=\"False\"/></Root>', " \
		         "'<?xml version=\"1.0\" encoding=\"GB2312\"?><Attachments/>', " \
		         "NULL, NULL, NULL, NULL, NULL, NULL, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, " \
		         "NULL, NULL, NULL, NULL, NULL, NULL, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000) "

		if not self.__debugMode:
			self.__mssql.sqlWork(sqlStr.format(company=self.__company, creator=self.__creator, receiverStr=self.__receiverStr,
			                                   msgTextStr=self.__msgTextStr, msgId=self.__msgId, title=self.__title,
			                                   sortMsg=self.__sortMsg))
		else:
			print(sqlStr.format(company=self.__company, creator=self.__creator, receiverStr=self.__receiverStr,
			                    msgTextStr=self.__msgTextStr, msgId=self.__msgId, title=self.__title,
			                    sortMsg=self.__sortMsg))
