from flask import current_app, Flask, redirect, Blueprint


urlTest = Blueprint('test', __name__)


@urlTest.route('/', methods=['GET'])
def testIndex():
	return 'test'


@urlTest.route('/download/<path:url>')
def testDownload(url):
	url2 = url.replace('/', '-')
	return redirect('/download/{}'.format(url2))

