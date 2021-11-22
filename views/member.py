from flask import Blueprint,request, jsonify

from utils import request_validator, email_validator, password_length_validator

from models.member import Member
from application.extensions import db 
from application.exceptions import ForemDataNotValid, EmailNotValid, PasswordLengthNotValid, DuplicateMemberFound, \
    RegisterFailed


blueprint = Blueprint('member', __name__, url_prefix='/api/v1/member')


@blueprint.route('/register', methods=['POST'])
def regirster():
    try:
        data = request.json
    
    except:
        raise ForemDataNotValid

    if not email_validator(data['email']):
        raise EmailNotValid

    if not password_length_validator(data['password']):
        raise PasswordLengthNotValid

    if not request_validator('MemberSerializer', data):
        raise ForemDataNotValid

    try:
        import pudb; pudb.set_trace()
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')

        hashed_password = Member.hash_password(password)
        member = Member(email, hashed_password, fullname)
        duplicate_member = Member.query \
            .filter(Member.email == member.email) \
            .first()

        if duplicate_member:
            raise DuplicateMemberFound()
        
    except:
        return jsonify("Register Exception"), 400

    try:
        db.session.add(member)
        db.session.commit()

    except Exception:
        db.session.rollback()

    return jsonify("Member Has Been Registered Successfully"), 200 


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
