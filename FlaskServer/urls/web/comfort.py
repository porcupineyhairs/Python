from flask import Blueprint, request, jsonify
from views.web.comfort.qc.jdy import QcPicture

web_comfort_blueprint = Blueprint('web_comfort_buleprint', __name__)


@web_comfort_blueprint.route('/qc/jdy', methods=['GET'])
def welcome():
	return 'Comfort Qc Jdy Welcome!'


@web_comfort_blueprint.route('/qc/jdy/get_picture/<string:wlno>', methods=['GET'])
def get_jdy_picture(wlno):
	print(wlno)
	qc_picture = QcPicture()
	
	return qc_picture.get_picture(wlno)
