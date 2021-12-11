import json
import datetime
import logging

from flask import g

MAIN_LOGGER = logging.getLogger('main_logger')
APPLICATION_LOGGER = logging.getLogger('application_logger')


def application_info_logger(status_code, message=None, action=None, username=None, **kwargs):
    logging.basicConfig(level=logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('main_logger').addHandler(console)

    MAIN_LOGGER.info(json.dumps({
        "logCode": status_code,
        'logMessage': message,
        'action': action,
        ' user': username,
        'time': datetime.datetime.now().isoformat(),
        'extra': kwargs
    }, separators=(',', ':')))


def application_warning_logger(status_code, message=None, action=None, username=None, **kwargs):
    APPLICATION_LOGGER.warning(json.dumps({
        "logCode": status_code,
        'logMessage': message,
        'action': action,
        'user': username,
        'time': datetime.datetime.now().isoformat(),
        'extra': kwargs
    }, separators=(',', ':')))


def application_error_logger(status_code, message=None, action=None, username=None, **kwargs):
    APPLICATION_LOGGER.error(json.dumps({
        "logCode": status_code,
        'logMessage': message,
        'action': action,
        ' user': username,
        'time': datetime.datetime.now().isoformat(),
        'extra': kwargs
    }, separators=(',', ':')))
