from flask import Blueprint, jsonify

from application.config import Config
from application.logger import application_info_logger


blueprint = Blueprint('version', __name__, url_prefix='/api/v1')


@blueprint.route('/version', methods=['GET'])
def version():
    application_info_logger(200, message=None, action="VERSION", username=None)
    return jsonify(Config.APP_VERSION), 200
