from flask import Blueprint,request, jsonify

from utils import request_validator, email_validator, password_length_validator

from application.exceptions import ForemDataNotValid, EmailNotValid, PasswordLengthNotValid


blueprint = Blueprint('member', __name__, url_prefix='/api/v1/member')


@blueprint.route('/register', methods=['POST'])
def regirster():
    try:
        data = request.json
    
    except:
        raise ForemDataNotValid

    if not email_validator(data['email']):
        raise EmailNotValid

    if not password_length_validator(data['hashed_password']):
        raise PasswordLengthNotValid

    if not request_validator('MemberSerializer', data):
        raise ForemDataNotValid

    return jsonify("Done"), 200 


@blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
    
    except:
        raise ForemDataNotValid
    
    if not request_validator('LoginMemberSerializer', data):
        raise ForemDataNotValid

    # TODO token, access token, refresh token
    return jsonify("Done"), 200 
