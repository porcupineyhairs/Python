from flask import Blueprint
from views.web.qc import QcPicture

web_blueprint = Blueprint('web_blueprint', __name__)


@web_blueprint.route('/', methods=['GET'])
def index():
	return 'WEB URL OK! '


@web_blueprint.route('/comfort/qc/jdy/get_picture/<string:wlno>', methods=['GET'])
def get_jdy_picture(wlno):
	qc_picture = QcPicture()
	return qc_picture.get_picture(wlno)
