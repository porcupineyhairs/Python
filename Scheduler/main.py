import json
from apscheduler.schedulers.blocking import BlockingScheduler
from modules.LogHelper import logger
import sys
import os


if __name__ == '__main__':
	root_path, file_name = os.path.split(sys.argv[0])
	scheduler = BlockingScheduler(timezone='Asia/Shanghai')
	file = open(root_path + os.sep + 'config.json', mode='r')
	json_str = file.read()
	config = json.loads(json_str)

	config_list = config.get('list', [])

	for config_tmp in config_list:
		path = config_tmp.get('path', '')
		file_name = config_tmp.get('file_name', '')
		class_name = config_tmp.get('class_name', '')
		import_str = 'import ' + path + '.' + file_name
		exec(import_str)

		sc = config_tmp['scheduler']
		trigger = sc.get('trigger', None)

		if trigger is not None:
			year = sc.get('year', None)
			month = sc.get('month', None)
			week = sc.get('week', None)
			day = sc.get('day', None)
			day_of_week = sc.get('day_of_week', None)
			hour = sc.get('hour', None)
			minute = sc.get('minute', None)
			second = sc.get('second', None)

			kwargs = {
				'trigger': trigger
			}

			if trigger == 'cron':
				kwargs.update({'year': year}) if year is not None else ''
				kwargs.update({'month': month}) if month is not None else ''
				kwargs.update({'week': week}) if week is not None else ''
				kwargs.update({'day': day}) if day is not None else ''
				kwargs.update({'day_of_week': day_of_week}) if day_of_week is not None else ''
				kwargs.update({'hour': hour}) if hour is not None else ''
				kwargs.update({'minute': minute}) if minute is not None else ''
				kwargs.update({'second': second}) if second is not None else ''
			if trigger == 'interval':
				kwargs.update({'weeks': week}) if week is not None else ''
				kwargs.update({'days': day}) if day is not None else ''
				kwargs.update({'hours': hour}) if hour is not None else ''
				kwargs.update({'minutes': minute}) if minute is not None else ''
				kwargs.update({'seconds': second}) if second is not None else ''

			if isinstance(class_name, list):
				for class_name_tmp in class_name:
					object_str = path + '.' + file_name + '.' + class_name_tmp + '()'
					exec('work = ' + object_str)
					if hasattr(work, 'main'):
						kwargs.update({'name': object_str})
						kwargs.update({'func': work.main})
						scheduler.add_job(**kwargs)
					else:
						logger.error(object_str + '  不存在main方法，跳过加入定时器')

			if isinstance(class_name, str):
				object_str = path + '.' + file_name + '.' + class_name + '()'
				exec('work = ' + object_str)
				if hasattr(work, 'main'):
					kwargs.update({'name': object_str})
					kwargs.update({'func': work.main})
					scheduler.add_job(**kwargs)
				else:
					logger.error(object_str + '  不存在main方法，跳过加入定时器')

	try:
		for index, job in enumerate(scheduler.get_jobs()):
			logger.warning('Main_定时任务列表 - ' + str(index) + ' - ' + str((job.name, job.trigger)))
		logger.warning('Main_定时任务开始')
		scheduler.start()

	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
		logger.warning('Main_定时任务关闭')

	except Exception as e:
		logger.warning('Main:{}'.format(str(e)))
