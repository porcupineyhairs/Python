
import os


class Config(object):
	APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
	APP_PORT = os.environ.get('APP_PORT', 8900)
	SECRET_KEY = os.environ.get('SECRET_KEY', 'this is a secret')
	DEBUG = os.environ.get('DEBUG', False)
	pass
