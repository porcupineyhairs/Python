
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
                "isAtAll": True
            }
        }
        return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content


class DingTalk_Disaster(DingTalk_Base):
    def __init__(self):
        super().__init__()
        # 填写机器人的url
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=a645d38e8b62f83752f3965ce34965dc34f42bb048625dc32949ccefd6add461'


if __name__ == '__main__':
    ding = DingTalk_Disaster()
    ding.send_msg('67890')
