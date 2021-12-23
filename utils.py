import re

from flask import request

from application.logger import application_error_logger
from serializers.member import MemberSerializer, LoginMemberSerializer
from serializers.access import AccessSerializer
from serializers.role import RoleSerializer
from application.config import Config
from application.exceptions import ValidationException, FormDataNotValid, EmptyForm


def get_json(log_action, member=None):
    if not request.json:
        application_error_logger(
            EmptyForm.status_code,
            message=EmptyForm.message,
            action=log_action,
            username=member,
        )
        raise EmptyForm

    try:
        data = request.json
        if not data:
            raise FormDataNotValid

    except Exception as e:
        application_error_logger(
            FormDataNotValid.status_code,
            message=f'{FormDataNotValid.message} - {str(e)}',
            action=log_action,
            username=member,
        )
        raise FormDataNotValid

    return data


def request_validator(serializer, data):
    try:
        if not eval(serializer)().validate(data):
            return True

        else:
            return False

    except Exception as e:
        raise ValidationException


def email_validator(email):
    try:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(email_pattern, email):
            return True

        else:
            return False

    except Exception as e:
        raise ValidationException


def password_length_validator(password):
    try:
        if len(password) < Config.MIN_PASSWORD_LENGTH or len(password) > Config.MAX_PASSWORD_LENGTH:
            return False

        else:
            return True

    except Exception as e:
        raise ValidationException
