from Crypto.Cipher import DES3
from binascii import b2a_base64, a2b_base64


class PrpCrypt(object):
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.mode = DES3.MODE_CBC
        self.iv = iv

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = DES3.new(self.key, self.mode, self.iv)
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ('\07' * add).encode('utf-8')
            print(text)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\07' * add).encode('utf-8')
            print(text)
        self.ciphertext = cryptor.encrypt(text)
        # return base64.b64encode(self.ciphertext)
        return b2a_base64(self.ciphertext)


    # EDS3解密
    def decrypt(self, text):
        cryptor = DES3.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_base64(text))
        return plain_text.decode("utf-8").rstrip("\07")


# pc = PrpCrypt(key=keys, iv=iv)  # 初始化密钥
# e = pc.encrypt(json.dumps(Json))  # 加密
# print("源数据:", json.dumps(Json))
# print("加密:", e)
# d = pc.decrypt(e)
# print("解密:", d)
# params = {
#     "param": e.decode("utf8")
# }
# print(params["param"])
# res = requests.post(url=url, data=params)
# print("============>", res.text)

pc = PrpCrypt(key='Harveyzyh', iv='12345678')  # 初始化密钥
e = pc.encrypt('12345678')  # 加密
# print("源数据:",)
print("加密:", e)
