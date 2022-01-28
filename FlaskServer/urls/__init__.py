from flask import Blueprint

root_blueprint = Blueprint('root_blueprint', __name__)


@root_blueprint.route('/', methods=['GET', 'POST'])
def index():
	return '<title>Flask</title><body><h1>Welcome Flask!</body>'
