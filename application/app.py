import importlib

from flask import Flask, jsonify

from .exceptions import ApplicationException


def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)

    for installed_app in app.config['INSTALLED_APPS']:
        view = importlib.import_module('views.{}'.format(installed_app))
        app.register_blueprint(view.blueprint)

    # Register the error handler
    @app.errorhandler(ApplicationException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.app_context().push()

    return app

