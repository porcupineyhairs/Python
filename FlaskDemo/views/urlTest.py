from flask import current_app, Flask, redirect, Blueprint


urlTest = Blueprint('test', __name__)


@urlTest.route('/', methods=['GET'])
def testIndex():
	return 'test'

