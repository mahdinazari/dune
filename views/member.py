from flask import Blueprint,request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from utils import request_validator, email_validator, password_length_validator

from models.member import Member
from application.config import Config
from application.extensions import db 
from application.exceptions import ForemDataNotValid, EmailNotValid, PasswordLengthNotValid, DuplicateMemberFound, \
    RegisterFailed, EmailNotInForm, PasswordNotInForm, MemberNotFound


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
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')

        hashed_password = Member.hash_password(password)
        member = Member(email, hashed_password, fullname)
        duplicate_member = Member.query \
            .filter(Member.email == member.email) \
            .first()
        
    except:
        return jsonify("Register Exception"), 400

    
    if duplicate_member:
        raise DuplicateMemberFound

    try:
        db.session.add(member)
        db.session.commit()

    except Exception:
        db.session.rollback()

    return jsonify("Member Has Been Registered Successfully"), 200 


@blueprint.route('/login', methods=['POST'])
def login():
    import pudb; pudb.set_trace()
    if not request.json:
        raise EmptyList()

    if 'email' not in request.json:
        raise EmailNotInForm()

    if 'password' not in request.json:
        raise PasswordNotInForm()

    try:
        data = request.json
    
    except:
        raise ForemDataNotValid
    
    if not request_validator('LoginMemberSerializer', data):
        raise ForemDataNotValid

    member = Member.query \
        .filter(Member.email == data['email']) \
        .first()

    if not member or member.is_deleted:
        raise MemberNotFound()
    
    if not check_password_hash(member.hashed_password, data['password']):
        raise MemberNotFound()

    access_token_expires = Config.JWT_ACCESS_TOKEN_EXPIRES
    refresh_token_expires = Config.JWT_REFRESH_TOKEN_EXPIRES
    payload = {"id": member.id, "email": member.email}
    access_token = create_access_token(
        identity=payload,
        expires_delta=access_token_expires,
        fresh=False
    )
     
    refresh_token = create_refresh_token(
        identity=payload,
        expires_delta=refresh_token_expires,
    )
    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    import pudb; pudb.set_trace()
    return jsonify(response), 200 


@blueprint.route('/sample', methods=['GET'])
@jwt_required
def sample():
    current_user = get_jwt_identity()
    return current_user
