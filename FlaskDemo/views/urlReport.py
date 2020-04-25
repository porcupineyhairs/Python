from flask import current_app, Flask, redirect, Blueprint


urlReport = Blueprint('report', __name__)


@urlReport.route('/', methods=['GET'])
def reportIndex():
	return 'reportIndex'

