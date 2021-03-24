import os


class Config(object):
	APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
	APP_PORT = os.environ.get('APP_PORT', 60031)
	SECRET_KEY = os.environ.get('SECRET_KEY', 'this is a secret')
	DEBUG = os.environ.get('DEBUG', True)
	pass
