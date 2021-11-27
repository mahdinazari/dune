from flask import Blueprint,request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, \
    get_jwt_identity, jwt_required, jwt_refresh_token_required

from utils import request_validator, email_validator, password_length_validator

from application.config import Config
from application.extensions import db
from application.redis_client import r
from models.member import Member, MemberSchema
from application.exceptions import FormDataNotValid, EmailNotValid, \
    PasswordLengthNotValid, DuplicateMemberFound, InsertDBFailed, \
    EmailNotInForm, PasswordNotInForm, MemberNotFound, EmptyForm


blueprint = Blueprint('member', __name__, url_prefix='/api/v1/member')


@blueprint.route('/register', methods=['POST'])
def register():
    if not request.json:
        raise EmptyForm

    try:
        data = request.json

    except Exception as e:
        raise FormDataNotValid

    is_valid = request_validator('MemberSerializer', data)
    if not is_valid:
        raise FormDataNotValid

    if not email_validator(data['email']):
        raise EmailNotValid

    if not password_length_validator(data['password']):
        raise PasswordLengthNotValid

    if not request_validator('MemberSerializer', data):
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
        return jsonify("Register Exception"), 400

    if duplicate_member:
        raise DuplicateMemberFound

    try:
        db.session.add(member)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise InsertDBFailed

    return jsonify("Member Has Been Registered Successfully"), 200


@blueprint.route('/login', methods=['POST'])
def login():
    if not request.json:
        raise EmptyForm

    if 'email' not in request.json:
        raise EmailNotInForm()

    if 'password' not in request.json:
        raise PasswordNotInForm()

    try:
        data = request.json

    except:
        raise FormDataNotValid

    if not request_validator('LoginMemberSerializer', data):
        raise FormDataNotValid

    member = Member.query \
        .filter(Member.email == data['email']) \
        .first()

    if not member or member.is_deleted:
        raise MemberNotFound()

    if not check_password_hash(member.hashed_password, data['password']):
        raise MemberNotFound()

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
        r.set(str(member.id), member.email)
        r.expire(str(member.id), Config.JWT_ACCESS_TOKEN_EXPIRES)

    except:
        pass

    return jsonify(response), 200


@blueprint.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@jwt_required
@blueprint.route('/get/<id>', methods=['GET'])
def get(id):
    schema = MemberSchema()
    member = Member.query.get_or_404(id)
    if member.is_deleted:
        return jsonify('404 Member Not Found'), 400

    return jsonify(schema.dump(member)), 200


@blueprint.route('/list', methods=['GET'])
@jwt_required
def list():
    members = Member.query.filter_by(removed_at=None).all()
    return jsonify(MemberSchema(many=True).dump(members)), 200

