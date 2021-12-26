from app import app


if __name__ == '__main__':
	app.logger.warning('Flask Server Starting')
	app.run(debug=app.config['APP_DEBUG'], port=app.config['APP_PORT'], host=app.config['APP_HOST'],
			threaded=app.config['APP_THREADED'])
