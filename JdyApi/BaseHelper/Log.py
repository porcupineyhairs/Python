import logging
from logging import handlers


class Logger(object):
	level_relations = {
		'debug': logging.DEBUG,
		'info': logging.INFO,
		'warning': logging.WARNING,
		'error': logging.ERROR,
		'crit': logging.CRITICAL
	}  # 日志级别关系映射
	
	def __init__(self,
	             filename='log.log',
	             level='info',
	             when='midnight',
	             backCount=3,
	             # fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
	             fmt='%(asctime)s - %(levelname)s: %(message)s',
	             ):

		self.logger = logging.getLogger(filename)
		# self.logger.propagate = False
		self.format_str = logging.Formatter(fmt)  # 设置日志格式
		self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
		sh = logging.StreamHandler()  # 往屏幕上输出
		sh.setFormatter(self.format_str)  # 设置屏幕上显示的格式

		# 指定间隔时间自动生成文件的处理
		# 实例化TimedRotatingFileHandler
		# interval是时间间隔，
		# backupCount是备份文件的个数，如果超过这个个数，就会自动删除，
		# when是间隔的时间单位， 单位有以下几种：
		# S 秒, M 分, H 小时, D 天, W 每星期(interval==0时代表星期一), midnight 每天凌晨
		# th = handlers.TimedRotatingFileHandler(filename=filename,
		#                                        when=when,
		#                                        # backupCount=backCount,
		#                                        encoding='utf-8')

		# 指定文件大小自动生成新的文件的处理
		# backupCount是备份文件的个数，如果超过这个个数，就会自动删除，
		# maxBytes是文件最大的大小， 如果是0，则忽略
		th = handlers.RotatingFileHandler(filename=filename, encoding='utf-8', maxBytes=0, backupCount=0)

		th.setFormatter(self.format_str)  # 设置文件里写入的格式

		if self.logger.handlers:  # 判断是否已添加handler，防止重复记录日志
			self.logger.handlers = []

		self.logger.addHandler(sh)  # 把对象加到logger里
		self.logger.addHandler(th)
