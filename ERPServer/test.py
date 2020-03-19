import os
from BaseHelper import Logger
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def text(t):
	print('{} ---- {}'.format(t, datetime.datetime.now()))


def kk():
	print(datetime.datetime.now())


if __name__ == '__main__':
	# __log_T = Logger(os.path.curdir + '/Log/test.log', level='info')
	# __log_T.logger.info('222' + '\n')

	# from SqlHelper import MsSqlHelper
	#
	# mssql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='WG_DB')
	#
	# sqlstr = r"select * from WG_APP_INF where 1=1"
	# getData = mssql.sqlWork(sqlstr)
	# print(getData)
	#
	# sqlstr = r"select * from WG_CONFIG where 1=1"
	# getData = mssql.sqlWork(sqlstr, getNoNone=True, getTitle=True)
	# print(getData)

	# from BaseHelper.ErpMsg import MsgHelper
	# erpMsg = MsgHelper(debug=False)
	# erpMsg.sendMsg(creator='Robot', title='订单完成领料通知',
	#                receivers=[['001114', '钟耀辉'], ['DS', '管理员']], msgText='订单号')

	# from ScheduleHelper.MOCTC2Y import MOCTC2YHelper
	#
	# try:
	# 	moctc2y = MOCTC2YHelper(debug=False)
	# 	returnStr = moctc2y.work()
	# 	__log_T.logger.info('MOCTC2Y:' + str(returnStr))
	# except Exception as e:
	# 	print(e)
	# 	__log_T.logger.info('MOCTC2Y:' + str(e))

	scheduler = BlockingScheduler()

	scheduler.add_job(func=kk, name='f1', id='f1', trigger='interval', seconds=5)
	scheduler.add_job(func=text, name='f3', id='f3', trigger='interval', seconds=2, args=['f3'])
	scheduler.add_job(func=text, name='f2', id='f2', trigger='interval', seconds=3, args=['f2'])
	print(datetime.datetime.now())
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
	print(scheduler.get_jobs())

	# pass
