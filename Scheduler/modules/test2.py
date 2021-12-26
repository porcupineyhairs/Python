import datetime
from modules.LogHelper import logger


class Test2:
	def __init__(self):
		logger.warning('test2 init')

	def __del__(self):
		pass

	def main(self):
		logger.info('test2')


class Test1:
	def __init__(self):
		logger.warning('test1 init')

	def __del__(self):
		pass

	def main(self):
		logger.info('test1')
