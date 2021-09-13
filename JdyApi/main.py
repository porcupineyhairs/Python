import datetime
import sys
from BaseHelper import Logger
from apscheduler.schedulers.blocking import BlockingScheduler

from Handler import LogTimeHandler, LogPlanHandler, BasicPlanHandler, GetRobotGxSumHandler, BasicPlanFixHandler
from ErpHandler import ErpSelloutScanHandler

loggerMain = Logger(sys.path[0] + '/Log/Main.log')
scheduler = BlockingScheduler()


# Jdy
def logTimeHandler():
	try:
		LogTimeHandler.main_work()
	except Exception as e:
		print(str(e))


def logPlanHandler():
	try:
		LogPlanHandler.main_work()
	except Exception as e:
		print(str(e))


def basicPlanHandler():
	try:
		BasicPlanHandler.main_work()
	except Exception as e:
		print(str(e))


def getRobotGxGxSum():
	try:
		GetRobotGxSumHandler.main_work()
	except Exception as e:
		print(str(e))


def basicPlanFixHandler():
	try:
		BasicPlanFixHandler.main_work()
	except Exception as e:
		print(str(e))


# Erp
def erpSelloutScanHandler():
	try:
		ErpSelloutScanHandler.main_work()
	except Exception as e:
		print(str(e))


if __name__ == '__main__':

	# basicPlanHandler()
	# logTimeHandler()
	# logPlanHandler()
	# getRobotGxGxSum()
	basicPlanFixHandler()
	# erpSelloutScanHandler()

	# scheduler.add_job(trigger='interval', seconds=30, func=logTimeHandler)
	# scheduler.add_job(trigger='interval', minutes=1, func=logPlanHandler)
	# scheduler.add_job(trigger='interval', seconds=30, func=getRobotGxGxSum)
	# scheduler.add_job(trigger='interval', seconds=30, func=basicPlanFixHandler)
	# scheduler.add_job(trigger='interval', minutes=1, func=erpSelloutScanHandler)

	# try:
	# 	loggerMain.logger.warning('Main_定时任务开始')
	# 	loggerMain.logger.warning('Main_现有任务:{}'.format(scheduler.get_jobs()))
	#
	# 	scheduler.start()
	#
	# except (KeyboardInterrupt, SystemExit):
	# 	scheduler.shutdown()
	# 	loggerMain.logger.warning('Main_定时任务关闭')
	# except Exception as e:
	# 	loggerMain.logger.error('Main:{}'.format(str(e)))
	# pass
