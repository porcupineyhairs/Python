import os
from BaseHelper import Logger
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from ScheduleHelper.MOCTC2Y import MOCTC2YHelper

__log_Main = Logger(os.path.curdir + '/Log/Main.log', level='info')

# 领料完成发送信息
moctc2y = MOCTC2YHelper(debug=False)


def mocMsgSend():
	try:
		returnStr = moctc2y.work()
		__log_Main.logger.info('MOCTC2Y:' + str(returnStr))
	except Exception as e:
		print(e)
		__log_Main.logger.info('MOCTC2Y:' + str(e))


if __name__ == '__main__':
	scheduler = BlockingScheduler()
	scheduler.add_job(func=mocMsgSend, name='mocMsgSend', id='mocMsgSend', trigger='interval', minutes=2,
	                  start_date='2020-03-19 00:00:00')

	try:
		__log_Main.logger.info('{} -- 定时任务开始'.format(datetime.datetime.now()))
		__log_Main.logger.info('{} -- 现有任务：{}'.format(datetime.datetime.now(), scheduler.get_jobs()))
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
		__log_Main.logger.info('{} -- 定时任务关闭\n\n'.format(datetime.datetime.now()))

