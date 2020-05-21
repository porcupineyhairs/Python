from flask import current_app


def flaskLog(mode='info', request=None, rtnDict=None):
	try:
		outDict = rtnDict if all([rtnDict]) else None
		if all([request]):
			ip = request.remote_addr
			url = request.url
			method = request.method
			inDict = request.json
		else:
			ip, url, method, inDict = '', '', '', ''

		logStr = ('{ip} - {url} - {method} - inData: {inData} - outData: {outData}'.
		          format(ip=ip,
		                 url=url,
		                 method=method,
		                 inData=inDict,
		                 outData=outDict)
		          )
		if mode == 'info':
			current_app.logger.info(logStr)
		if mode == 'error':
			current_app.logger.error(logStr)

		if mode == 'warning':
			current_app.logger.warning(logStr)
	except Exception as e:
		current_app.logger.error('Logger Error : {}'.format(str(e)))
