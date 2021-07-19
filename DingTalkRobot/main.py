
import requests
import json


class DingTalk_Base:
	def __init__(self):
		self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
		self.url = ''

	def send_msg(self, text):
		json_text = {
			"msgtype": "text",
			"text": {
				"content": text
			},
			"at": {
				"atMobiles": [
					""
				],
				"isAtAll": False
			}
		}
		return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content


class DingTalk_Disaster(DingTalk_Base):
	def __init__(self):
		super().__init__()
		# 填写机器人的url
		self.url = 'https://oapi.dingtalk.com/robot/send?access_token=83dee730d02f1719468371e2574d931619f92d3471959028263a8309f6a96a58'


if __name__ == '__main__':
	ding = DingTalk_Disaster()
	ding.send_msg('冯国涛')
