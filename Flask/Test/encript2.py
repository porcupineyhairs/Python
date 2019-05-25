#AES-demo

import base64
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''

key = 'HarveyZYH00Flask'
before = r'"Uid": "001114", "Mode": "Complete", "Parameter": "JH201812281329460001", "Data": "", "RowCount": "4"'
after = ''


# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
	while len(value) % 16 != 0:
		value += '\0'
	return str.encode(value)  # 返回bytes


# 加密方法
def AES16Encrypt():
	# 秘钥
	# key = '1234567890abcdef'
	# 待加密文本
	# text = r'"Uid": "001114", "Mode": "Complete", "Parameter": "JH201812281329460001", "Data": "", "RowCount": "4"'
	text = before
	# 初始化加密器
	aes = AES.new(add_to_16(key), AES.MODE_ECB)
	# 先进行aes加密
	encrypt_aes = aes.encrypt(add_to_16(text))
	# 用base64转成字符串形式
	encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
	global after
	after = encrypted_text
	print(encrypted_text)
	
	
# 解密方法
def AES16Decrypt():
	# 秘钥
	# key = '1234567890abcdef'
	# # 密文
	# text = (r'L3tDvmVacjU5ifBeW0rGO43Qrcwt6ID5OMZyxxvpp6vYbyX90jDcBCHLnzPNF2aiVWmIrQEiuDbe'
	#         r'hjDImJ/JgZjAk6f/joYnITSnijmmT0lt5vFb483Ai/w+D35J/prHWxCX+L0kbJjI4UFh4WU9+w==')
	text = after
	# 初始化加密器
	aes = AES.new(add_to_16(key), AES.MODE_ECB)
	# 优先逆向解密base64成bytes
	base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
	# 执行解密密并转码返回str
	decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
	print(decrypted_text)


if __name__ == '__main__':
	print(before)
	print()
	AES16Encrypt()
	AES16Decrypt()
