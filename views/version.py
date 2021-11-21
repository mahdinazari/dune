from flask import Blueprint, jsonify

from application.config import Config


blueprint = Blueprint('version', __name__, url_prefix='/api/v1')


@blueprint.route('/version', methods=['GET'])
def version():
    return jsonify(Config.APP_VERSION), 200
