from base64 import b64encode
from Crypto.Cipher import AES


def getaespwd(key, value):
	text = value
	padding = '\0'

	cryptor = AES.new(key, AES.MODE_CBC, padding * 16)
	length = 16
	count = len(text)
	if count < length:
		add = (length - count)
		text += (chr(add) * add)

	ciphertext = cryptor.encrypt(text)
	return b64encode(ciphertext)


key = "klsjdkfjdkjfkd"  # 秘钥
value = "123456"  # 被加密字符
aes128string = getaespwd(key, value)
print(aes128string)
