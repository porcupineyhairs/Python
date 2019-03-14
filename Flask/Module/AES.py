import base64
from Crypto.Cipher import AES
import json


class AES16:
	def __init__(self):
		# 秘钥
		self.__key = 'HarveyZYH00Flask'
		# 初始化加密器
		self.__aes = AES.new(self.__add_to_16(self.__key), AES.MODE_ECB)
	
	def __add_to_16(self, value):
		while len(value) % 16 != 0:
			value += '\0'
		return str.encode(value)  # 返回bytes
	
	def Encrypt(self, text):
		# 先进行aes加密
		encrypt_aes = self.__aes.encrypt(self.__add_to_16(text))
		# 用base64转成字符串形式
		encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
		return encrypted_text
	
	def Decrypt(self, text):
		# 优先逆向解密base64成bytes
		base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
		# 执行解密密并转码返回str
		decrypted_text = str(self.__aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
		return decrypted_text


class EncryptDict:
	def __init__(self):
		self.__aes16 = AES16()
		self.__strIn = None
		self.__strOut = None
		self.__dictIn = None
		self.__dictOut = None
	
	def Encrypt(self, dictIn):
		self.__init__()
		self.__dictIn = dictIn
		self.__strOut = self.__aes16.Encrypt(json.dumps(self.__dictIn))
		return self.__strOut
	
	def Decrypt(self, strIn):
		self.__init__()
		self.__strIn = strIn
		self.__dictOut = json.loads(self.__aes16.Decrypt(self.__strIn))
		return self.__dictOut
