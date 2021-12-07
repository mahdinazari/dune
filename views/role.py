from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from application.extensions import db
from models.role import Role, RoleSchema
from models.member import Member, MemberSchema
from application.exceptions import FormDataNotValid, DuplicateRoleFound, InsertDBFailed
from serializers.role import RoleSerializer
from utils import request_validator

blueprint = Blueprint('role', __name__, url_prefix='/api/v1/role')


@blueprint.route('/create', methods=['POST'])
@jwt_required
def create():
    try:
        data = request.json

    except Exception as e:
        raise FormDataNotValid

    if 'title' not in request.json:
        raise FormDataNotValid

    is_valid = request_validator('RoleSerializer', data)
    if not is_valid:
        raise FormDataNotValid

    role = Role.query.filter_by(title=data['title']).first()
    if role:
        raise DuplicateRoleFound

    try:
        role = Role(data['title'])
        db.session.add(role)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise InsertDBFailed

    schema = RoleSchema()
    return jsonify(schema.dump(role)), 200


@blueprint.route('/add/<role_id>/member/<member_id>', methods=['GET'])
@jwt_required
def add(role_id, member_id):
    try:
        member = Member.query.get_or_404(member_id)
        role = Role.query.get_or_404(role_id)

    except Exception as e:
        raise FormDataNotValid

    try:
        member.role = role
        member.role_id = role_id
        db.session.add(member)
        db.session.commit()

    except Exception as e:
        raise InsertDBFailed

    schema = MemberSchema()
    return jsonify(schema.dump(member)), 200
