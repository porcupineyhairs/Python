from flask import current_app, Flask, redirect, Blueprint


urlReport = Blueprint('report', __name__)


@urlReport.route('/', methods=['GET'])
def reportIndex():
	return 'reportIndex'


@urlReport.route('/download/<path:url>')
def reportDownload(url):
	url2 = url.replace('/', '-')
	return redirect('/download/{}'.format(url2))


@urlReport.route('/redirect/<path:url>')
def reportRedirect(url):
	return redirect('/' + url)

