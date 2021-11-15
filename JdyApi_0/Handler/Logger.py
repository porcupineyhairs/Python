class Logger:
	def __init__(self, module_name=''):
		self.__module_name = module_name

	def log(self, strs=None):
		if strs:
			print(self.__module_name + ' -- ' + str(strs))
		else:
			print(self.__module_name)
