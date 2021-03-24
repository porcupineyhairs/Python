from flask import current_app
from json import loads


def flaskLog(request, rtnDict):
	current_app.logger.info('{ip} - {url} - {method} - inData: {inData} - outData: {outData}'.
	                        format(ip=request.remote_addr, url=request.url, method=request.method,
	                               inData=loads(request.get_data()),
	                               outData=rtnDict)
	                        )
