import sys
from BaseHelper import Logger
from apscheduler.schedulers.blocking import BlockingScheduler
from ScheduleHelper import MOCTC2YHelper, AutoErpPlanHelper, INVMBBoxSize, GetBomList

loggerMain = Logger(sys.path[0] + '/Log/Main.log')
scheduler = BlockingScheduler()

# 领料完成发送信息
moctc2y = MOCTC2YHelper(debug=False, host='192.168.0.99', logger=loggerMain)

# 生成ERP计划
autoPlan = AutoErpPlanHelper(debug=False, host='192.168.0.99', logger=loggerMain)

# 获取纸箱的尺寸及体积
invmbBoxSize = INVMBBoxSize(host='192.168.0.99', logger=loggerMain)

# 获取标准bom物料明细
getBomList = GetBomList(host='192.168.0.99', logger=loggerMain)


def mocMsgWork():
	try:
		moctc2y.work()
	except Exception as exc:
		loggerMain.logger.error('MOCTC2Y: ' + str(exc))


def autoPlanWork():
	try:
		if not autoPlan.workingFlag:
			autoPlan.work()
	except Exception as exc:
		loggerMain.logger.error('AutoErpPlan: ' + str(exc))


def invmbBoxSizeWork():
	try:
		invmbBoxSize.work()
	except Exception as exc:
		loggerMain.logger.error('InvmbBoxSize: ' + str(exc))


def getBomListWork():
	try:
		getBomList.work()
	except Exception as exc:
		loggerMain.logger.error('GetBomList: ' + str(exc))


if __name__ == '__main__':
	# scheduler.add_job(func=mocMsgWork, name='MocMsgWork', id='MocMsgWork', trigger='interval', minutes=20,
	#                   start_date='2020-03-19 00:00:00')
	scheduler.add_job(func=autoPlanWork, name='AutoErpPlan', id='AutoErpPlan', trigger='interval', hours=1,
	                  start_date='2020-03-30 00:00:00')
	scheduler.add_job(func=invmbBoxSizeWork, name='INVMBBoxSize', id='INVMBBoxSize', trigger='interval', weeks=1,
	                  hours=2, start_date='2020-03-30 00:00:00')
	scheduler.add_job(func=getBomListWork, name='GetBomList', id='GetBomList', trigger='interval', weeks=1, hours=3,
	                  start_date='2020-03-30 00:00:00')

	try:
		loggerMain.logger.warning('Main_定时任务开始')
		loggerMain.logger.warning('Main_现有任务:{}'.format(scheduler.get_jobs()))

		loggerMain.logger.warning('Main_执行需优先处理任务')
		autoPlanWork()

		scheduler.start()

	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
		loggerMain.logger.warning('Main_定时任务关闭')
	except Exception as e:
		loggerMain.logger.error('Main:{}'.format(str(e)))
