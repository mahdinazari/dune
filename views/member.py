from flask import Blueprint,request, jsonify

from utils import request_validator, email_validator, password_length_validator

from application.exceptions import ForemDataNotValid, EmailNotValid, PasswordLengthNotValid


blueprint = Blueprint('member', __name__, url_prefix='/api/v1')


@blueprint.route('/member/register', methods=['POST'])
def regirster():
    data = request.json
    if not email_validator(data['email']):
        raise EmailNotValid

    if not password_length_validator(data['hashed_password']):
        raise PasswordLengthNotValid

    if not request_validator('MemberSerializer', data):
        raise PasswordPatternNotValid

    return jsonify("Done"), 200 
