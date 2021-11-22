import os
from datetime import timedelta

from dotenv import load_dotenv


class Config:
    DEBUG = False

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ASDASDOWIQ!@&EQHC<XNYWGYW#!@')
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '@ASDASDOWIQ!@&EQHC<XNYWGYW#!@')
    JWT_EXPIRES_DELTA = timedelta(days=10)


    # SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_BINDS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')
   
    # Apps
    INSTALLED_APPS = [
        'version',
        'member',
    ]

    # Version
    APP_VERSION = 'v0.1.0'

    # Application config
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 25


class DevelopConfig(Config):
    DEBUG = True


class TestConfig(DevelopConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
