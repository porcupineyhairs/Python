import sys
from BaseHelper import Logger
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from ScheduleHelper.MOCTC2Y import MOCTC2YHelper
from ScheduleHelper.GeneratePlan import GeneratePlanHelper

loggerMain = Logger(sys.path[0] + '/Log/Main.log')
scheduler = BlockingScheduler()

# 领料完成发送信息
moctc2y = MOCTC2YHelper(debug=False)

# 生成ERP计划
generatePlan = GeneratePlanHelper(debug=True, logger=loggerMain, host='192.168.1.61')


def mocMsgSend():
	try:
		returnStr = moctc2y.work()
		loggerMain.logger.info('MOCTC2Y: ' + str(returnStr))
	except Exception as e:
		loggerMain.logger.error('MOCTC2Y: ' + str(e))


def generatePlans():
	try:
		generatePlan.work()
	except Exception as e:
		loggerMain.logger.error('GeneratePlan: ' + str(e))


if __name__ == '__main__':
	# scheduler.add_job(func=mocMsgSend, name='mocMsgSend', id='mocMsgSend', trigger='interval', minutes=20,
	#                   start_date='2020-03-19 00:00:00')
	scheduler.add_job(func=generatePlans, name='generatePlan', id='GeneratePlan', trigger='interval', minutes=1,
	                  start_date='2020-03-19 00:00:00')

	try:
		loggerMain.logger.warning('Main_定时任务开始')
		loggerMain.logger.warning('Main_现有任务:{}'.format(scheduler.get_jobs()))
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
		loggerMain.logger.warning('Main_定时任务关闭')
	except Exception as e:
		loggerMain.logger.error('Main:{}'.format(str(e)))

