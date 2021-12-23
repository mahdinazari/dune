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
    try:
        MAIN_LOGGER.info(json.dumps({
            "logCode": status_code,
            'logMessage': str(message),
            'action': str(action),
            'user': str(username),
            'time': datetime.datetime.now().isoformat(),
            'extra': kwargs
        }, separators=(',', ':')))
    
    except Exception as e:
        application_error_logger(400, message=str(e), action="LOGGING__"+action, username=None)
        return


def application_warning_logger(status_code, message=None, action=None, username=None, **kwargs):
    logging.basicConfig(level=logging.WARNING)
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    logging.getLogger('main_logger').addHandler(console)
    try:
        APPLICATION_LOGGER.warning(json.dumps({
            "logCode": status_code,
            'logMessage': str(message),
            'action': str(action),
            'user': str(username),
            'time': datetime.datetime.now().isoformat(),
            'extra': kwargs
        }, separators=(',', ':')))
        
    except Exception as e:
        application_error_logger(400, message=str(e), action="LOGGING__"+action, username=None)


def application_error_logger(status_code, message=None, action=None, username=None, **kwargs):
    logging.basicConfig(level=logging.ERROR)
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logging.getLogger('main_logger').addHandler(console)
    try:
        MAIN_LOGGER.error(json.dumps({
            "logCode": status_code,
            'logMessage': str(message),
            'action': str(action),
            'user': str(username),
            'time': datetime.datetime.now().isoformat(),
            'extra': kwargs
        }, separators=(',', ':')))
    
    except:
        pass
    