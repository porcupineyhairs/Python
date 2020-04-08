import random


class CreateRandomCode:
	@staticmethod
	def getRandomStr():
		'''获取一个随机字符串，每个字符的颜色也是随机的'''
		random_num = str(random.randint(0, 9))
		random_low_alpha = chr(random.randint(97, 122))
		random_upper_alpha = chr(random.randint(65, 90))
		random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
		return random_char

	@staticmethod
	def randomCodeGenerate(lenth=16):
		'''根据传入的需求长度，返回随机码'''
		code = ''
		for i in range(lenth):
			code += CreateRandomCode.getRandomStr()
		return code.upper()

	@staticmethod
	def get32bRandomCode():
		return CreateRandomCode.randomCodeGenerate(32)

	@staticmethod
	def get16bRandomCode():
		return CreateRandomCode.randomCodeGenerate(16)
