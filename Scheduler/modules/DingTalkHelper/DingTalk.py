import datetime
import requests
import json


class DingTalk_Base:
	def __init__(self, url=''):
		self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
		self.url = url
	
	def send_msg(self, text, mobile=[""]):
		json_text = {
			"msgtype": "text",
			"text": {
				"content": text
			},
		}
		if mobile == 'all':
			json_text.update({"at": {
				"atMobiles": mobile,
				"isAtAll": True
			}})
		else:
			json_text.update({"at": {
				"atMobiles": mobile,
				"isAtAll": False
			}})
		return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content


class DingTalk_Disaster(DingTalk_Base):
	def __init__(self, url):
		super().__init__()
		# 填写机器人的url
		self.url = url
