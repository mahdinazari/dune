import os
import json
from datetime import timedelta

from dotenv import load_dotenv


class Config:
    DEBUG = False

    # Session
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Keys
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # JWT
    JWT_COOKIE_SECURE = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_EXPIRES_DELTA = timedelta(days=10)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=200)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_BINDS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'PRODUCTION_DATABASE_URL',
        'postgres://postgres:postgres@localhost/dune'
    )

    # Apps
    INSTALLED_APPS = [
        'version',
        'member',
        'role',
    ]
    # Version
    APP_VERSION = 'v0.1.0'

    # Application config
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 25

    # Redis
    REDIS_HOST = os.environ.get('REDIS_HOST', '')
    REDIS_PORT = os.environ.get('REDIS_PORT', '')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
    REDIS_DB = os.environ.get('REDIS_DB', 10)

    # Logger
    LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST")
    LOGSTASH_PORT = os.environ.get("LOGSTASH_PORT")
    USE_SELF_LOG_CONF = os.environ.get("USE_SELF_LOG_CONF")
    try:
        LOGGER_CONFIG_PATH = os.environ.get("LOGGER_CONFIG_PATH")
        logger_conf_file = open(LOGGER_CONFIG_PATH + '/log_conf.json', 'r')

    except Exception as e:
        logger_conf_file = open(os.path.dirname(os.path.abspath(__file__)) + '/log_conf.json', 'r')

    LOGGER_CONFIG = json.loads(logger_conf_file.read())

    USER_ROLE_NAME = 'user'
    ADMIN_ROLE_NAME = 'admin'


class DevelopConfig(Config):
    DEBUG = True


class TestConfig(DevelopConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
