from flask import current_app, Flask, redirect, Blueprint
from modules.Api import *


urlApi = Blueprint('api', __name__)


@urlApi.route('/', methods=['GET'])
def apiIndex():
	return 'api'
