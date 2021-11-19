import importlib

from flask import Flask


def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)

    for installed_app in app.config['INSTALLED_APPS']:
        view = importlib.import_module('views.{}'.format(installed_app))
        app.register_blueprint(view.blueprint)

    return app

