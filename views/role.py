from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from application.extensions import db
from models.role import Role, RoleSchema
from models.member import Member, MemberSchema
from utils import request_validator, get_json
from application.decorators import admin_required
from application.logger import application_info_logger, application_error_logger
from application.exceptions import FormDataNotValid, DuplicateRoleFound, InsertDBFailed


blueprint = Blueprint('role', __name__, url_prefix='/api/v1/role')


@blueprint.route('/create', methods=['POST'])
@jwt_required
@admin_required
def create():
    log_action = 'CREATE_ROLE'
    username = Member.current_member().email
    data = get_json(log_action)
    if 'title' not in data:
        application_error_logger(
            FormDataNotValid.status_code,
            action=log_action,
            username=username,
            message=FormDataNotValid.message
        )
        raise FormDataNotValid

    is_valid = request_validator('RoleSerializer', data)
    if not is_valid:
        application_error_logger(
            FormDataNotValid.status_code,
            action=log_action,
            username=username,
            message=FormDataNotValid.message
        )
        raise FormDataNotValid

    role = Role.query.filter_by(title=data['title']).first()
    if role:
        application_error_logger(
            DuplicateRoleFound.status_code,
            action=log_action,
            username=username,
            message=DuplicateRoleFound.message
        )
        raise DuplicateRoleFound

    try:
        role = Role(data['title'])
        db.session.add(role)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        application_error_logger(
            InsertDBFailed.status_code,
            action=log_action,
            username=username,
            message=InsertDBFailed.message
        )
        raise InsertDBFailed

    schema = RoleSchema()
    application_info_logger(
        200,
        action=log_action,
        username=username,
        message="Role Has Been Created"
    )
    return jsonify(schema.dump(role)), 200


@blueprint.route('/assign/<role_id>/member/<member_id>', methods=['GET'])
@jwt_required
@admin_required
def assign(role_id, member_id):
    log_action = 'ASSIGN_ROLE'
    username = Member.current_member().email
    try:
        member = Member.query.get_or_404(member_id)
        role = Role.query.get_or_404(role_id)

    except Exception as e:
        application_error_logger(
            FormDataNotValid.status_code,
            action=log_action,
            username=username,
            message=FormDataNotValid.message
        )
        raise FormDataNotValid

    try:
        member.role = role
        member.role_id = role_id
        db.session.add(member)
        db.session.commit()

    except Exception as e:
        application_error_logger(
            InsertDBFailed.status_code,
            action=log_action,
            username=username,
            message=InsertDBFailed.message
        )
        raise InsertDBFailed

    application_info_logger(
        200,
        message='Role Assigned Successfully',
        action=log_action,
        username=member.email,
        extra={"requested member": str(role.title)}
    )
    schema = MemberSchema()
    return jsonify(schema.dump(member)), 200
