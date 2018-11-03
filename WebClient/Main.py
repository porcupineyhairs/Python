import requests
import json

user_info = {'name': 'me', 'password': 'me'}
r = requests.post("http://192.168.31.136/client", data=json.dumps(user_info))

print(r.json())
