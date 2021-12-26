import datetime
from modules.LogHelper import logger


class Test1:
	def __init__(self):
		logger.warning('test1 init')

	def __del__(self):
		pass

	def main(self):
		logger.info('test1')
