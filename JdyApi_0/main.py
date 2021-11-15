import datetime
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

from Handler import LogTimeHandler, LogPlanHandler, GetRobotGxSumHandler, BasicPlanFixHandler

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


if __name__ == '__main__':
	# logTimeHandler()
	# logPlanHandler()
	# getRobotGxGxSum()
	# basicPlanFixHandler()

	scheduler.add_job(trigger='interval', minutes=1, func=logTimeHandler)
	scheduler.add_job(trigger='interval', minutes=1, func=logPlanHandler)
	scheduler.add_job(trigger='interval', minutes=1, func=getRobotGxGxSum)
	scheduler.add_job(trigger='interval', minutes=1, func=basicPlanFixHandler)

	try:
		print('Main_定时任务开始')
		scheduler.start()

	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
		print('Main_定时任务关闭')
	except Exception as e:
		print('Main:{}'.format(str(e)))
	pass
