import os
import sys


class Config(object):
	APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
	APP_PORT = os.environ.get('APP_PORT', 8900)
	SECRET_KEY = os.environ.get('SECRET_KEY', 'this is a secret')
	DEBUG = os.environ.get('DEBUG', True)
	LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', sys.path[0] + '/log/flask.log')
	pass
