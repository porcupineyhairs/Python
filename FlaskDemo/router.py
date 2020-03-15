from flask import current_app, Flask, redirect, Blueprint


urls_1 = Blueprint('u1', __name__)


@urls_1.route('/', methods=['GET'])
def test0():
	return 'aaaa'

