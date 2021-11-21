import re

from serializers.member import MemberSerializer

from application.config import Config


def request_validator(serializer, data):
    if not eval(serializer)().validate(data):
        return True
    
    else:
         return False


def email_validator(email):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(email_pattern, email)):
        return True
    
    else:
        return False


def password_length_validator(password):
    if len(password) < Config.MIN_PASSWORD_LENGTH or len(password) > Config.MAX_PASSWORD_LENGTH:
        return False

    else:
        return True
        