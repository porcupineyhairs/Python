import sys
from BaseHelper import Logger
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from ScheduleHelper import MOCTC2YHelper, AutoErpPlanHelper

loggerMain = Logger(sys.path[0] + '/Log/Main.log')
scheduler = BlockingScheduler()

# 领料完成发送信息
moctc2y = MOCTC2YHelper(debug=False, host='192.168.0.99', logger=loggerMain)

# 生成ERP计划
autoPlan = AutoErpPlanHelper(debug=False, host='192.168.0.99', logger=loggerMain)


def mocMsgWork():
	try:
		moctc2y.work()
	except Exception as e:
		loggerMain.logger.error('MOCTC2Y: ' + str(e))


def autoPlanWork():
	try:
		if not autoPlan.workingFlag:
			autoPlan.work()
	except Exception as e:
		loggerMain.logger.error('AutoErpPlan: ' + str(e))


if __name__ == '__main__':
	scheduler.add_job(func=mocMsgWork, name='MocMsgWork', id='MocMsgWork', trigger='interval', minutes=20,
	                  start_date='2020-03-19 00:00:00')
	scheduler.add_job(func=autoPlanWork, name='AutoErpPlan', id='AutoErpPlan', trigger='interval', minutes=30,
	                  start_date='2020-03-30 00:00:00')

	try:
		loggerMain.logger.warning('Main_定时任务开始')
		loggerMain.logger.warning('Main_现有任务:{}'.format(scheduler.get_jobs()))
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
		loggerMain.logger.warning('Main_定时任务关闭')
	except Exception as e:
		loggerMain.logger.error('Main:{}'.format(str(e)))
