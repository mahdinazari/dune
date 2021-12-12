from flask import Blueprint,request, jsonify, session
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, \
    get_jwt_identity, jwt_required, jwt_refresh_token_required

from utils import request_validator, email_validator, password_length_validator

from application.config import Config
from application.extensions import db
from application.redis_client import r
from models.member import Member, MemberSchema
from application.logger import application_info_logger, application_error_logger
from application.exceptions import FormDataNotValid, EmailNotValid, \
    PasswordLengthNotValid, DuplicateMemberFound, InsertDBFailed, \
    EmailNotInForm, PasswordNotInForm, MemberNotFound, EmptyForm


blueprint = Blueprint('member', __name__, url_prefix='/api/v1/member')


@blueprint.route('/register', methods=['POST'])
def register():
    log_action = 'MEMBER_REGISTER'
    if not request.json:
        application_error_logger(
            EmptyForm.status_code,
            message=EmptyForm.message,
            action=log_action, 
            username=None,
        )
        raise EmptyForm

    try:
        data = request.json

    except Exception as e:
        application_error_logger(
            FormDataNotValid.status_code,
            message=f'{FormDataNotValid.message} - {str(e)}',
            action=log_action, 
            username=None,
        )
        raise FormDataNotValid

    is_valid = request_validator('MemberSerializer', data)
    if not is_valid:
        application_error_logger(
            FormDataNotValid.status_code,
            message=FormDataNotValid.message,
            action=log_action, 
            username=None,
        )
        raise FormDataNotValid

    if not email_validator(data['email']):
        application_error_logger(
            EmailNotValid.status_code,
            message=EmailNotValid.message,
            action=log_action, 
            username=None,
        )
        raise EmailNotValid

    if not password_length_validator(data['password']):
        application_error_logger(
            PasswordLengthNotValid.status_code,
            message=PasswordLengthNotValid.message,
            action=log_action, 
            username=None,
        )
        raise PasswordLengthNotValid

    if not request_validator('MemberSerializer', data):
        application_error_logger(
            PasswordLengthNotValid.status_code,
            message=FormDataNotValid.message,
            action=log_action, 
            username=None,
        )
        raise FormDataNotValid

    try:
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')

        hashed_password = Member.hash_password(password)
        member = Member(email, hashed_password, fullname)
        duplicate_member = Member.query \
            .filter(Member.email == member.email) \
            .first()

    except Exception as e:
        application_error_logger(
            400,
            message=f'Register Exception! - {str(e)}',
            action=log_action, 
            username=member.email,
        )
        return jsonify("Register Exception"), 400

    if duplicate_member:
        application_error_logger(
            DuplicateMemberFound.status_code,
            message=DuplicateMemberFound.message,
            action=log_action, 
            username=member.email,
        )
        raise DuplicateMemberFound

    try:
        db.session.add(member)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        application_error_logger(
            InsertDBFailed.status_code,
            message=f'{InsertDBFailed.message} - {str(e)}',
            action=log_action,
            username=member.email
        )
        raise InsertDBFailed

    message = "Member Has Been Registered Successfully"
    application_info_logger(200, message=message, action=log_action, username=member.email)
    return jsonify(message), 200


@blueprint.route('/login', methods=['POST'])
def login():
    log_action = "LOGIN"
    if not request.json:
        application_error_logger(
            EmptyForm.status_code,
            message=EmptyForm.message,
            action=log_action,
            username=None,
        )
        raise EmptyForm

    if 'email' not in request.json:
        application_error_logger(
            EmailNotInForm.status_code,
            message=EmailNotInForm.message,
            action=log_action,
            username=None,
        )
        raise EmailNotInForm

    if 'password' not in request.json:
        application_error_logger(
            PasswordNotInForm.status_code,
            message=PasswordNotInForm.message,
            action=log_action,
            username=None,
        )
        raise PasswordNotInForm

    try:
        data = request.json

    except Exception as e:
        application_error_logger(
            FormDataNotValid.status_code,
            message=f'{FormDataNotValid.message} - {str(e)}',
            action=log_action,
            username=None,
        )
        raise FormDataNotValid

    if not request_validator('LoginMemberSerializer', data):
        application_error_logger(
            FormDataNotValid.status_code,
            message=FormDataNotValid.message,
            action=log_action,
            username=None,
        )
        raise FormDataNotValid

    member = Member.query \
        .filter(Member.email == data['email']) \
        .first()

    if not member or member.is_deleted:
        application_error_logger(
            MemberNotFound.status_code,
            message=MemberNotFound.message,
            action=log_action,
            username=None,
        )
        raise MemberNotFound

    if not check_password_hash(member.hashed_password, data['password']):
        application_error_logger(
            MemberNotFound.status_code,
            message=MemberNotFound.message,
            action=log_action,
            username=None,
        )
        raise MemberNotFound

    access_token_expires = Config.JWT_ACCESS_TOKEN_EXPIRES
    refresh_token_expires = Config.JWT_REFRESH_TOKEN_EXPIRES
    identity = {"id": str(member.id), "email": member.email}
    access_token = create_access_token(
        identity=identity,
        expires_delta=access_token_expires,
        fresh=False
    )

    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=refresh_token_expires,
    )
    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    
    try:
        import pudb; pudb.set_trace()
        session['user'] = identity
        r.set(str(member.id), member.email)
        r.expire(str(member.id), Config.JWT_ACCESS_TOKEN_EXPIRES)

    except Exception as e:
        application_error_logger(
            400,
            message=str(e),
            action=log_action,
            username=None,
        )
    
    application_info_logger(200, message="Login Successfully", action=log_action, username=data['email'])
    return jsonify(response), 200


@blueprint.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    log_action = 'REFRESH'
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        
    except Exception as e:
        application_error_logger(
            400,
            message=f'Generate Refresh Token Exception - {str(e)}',
            action=log_action,
            username=None,
        )
        
    application_info_logger(
        200,
        message='Refresh Token Has Been Generated',
        action=log_action,
        username=identity['email'],
    )
    return jsonify(access_token=access_token)


@blueprint.route('/get/<id>', methods=['GET'])
@jwt_required
def get(id):
    log_action = 'MEMBER_GET'
    schema = MemberSchema()
    import pudb; pudb.set_trace()
    try:
        member = Member.query.get_or_404(id)
    
    except Exception as e:
        application_error_logger(
            MemberNotFound.status_code,
            message=MemberNotFound.message,
            action=log_action,
            username=None,
        )
        raise MemberNotFound
    
    if member.is_deleted or not member:
        application_error_logger(
            MemberNotFound.status_code,
            message=MemberNotFound.message,
            action=log_action,
            username=g.user['email'],
        )
        return jsonify('404 Member Not Found'), 404
        
    application_info_logger(
        200,
        message='Request Successed',
        action=log_action,
        username=None,
    )
    return jsonify(schema.dump(member)), 200


@blueprint.route('/list', methods=['GET'])
@jwt_required
def list():
    members = Member.query.filter_by(removed_at=None).all()
    return jsonify(MemberSchema(many=True).dump(members)), 200

