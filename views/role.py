from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from application.extensions import db
from models.role import Role, RoleSchema
from models.member import Member, MemberSchema
from utils import request_validator, get_json, uuid_validator
from application.decorators import admin_required
from application.logger import application_info_logger, application_error_logger
from application.exceptions import FormDataNotValid, DuplicateRoleFound, InsertDBFailed, FetchDataException, \
    RoleNotFound

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
            message=InsertDBFailed.message,
            extra={"exception": str(e)}
        )
        raise InsertDBFailed

    schema = RoleSchema()
    application_info_logger(
        200,
        action=log_action,
        username=username,
        message="Role Has Been Created",
        extra={"role": str(role.title)}
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
            message=FormDataNotValid.message,
            extra={"exception": str(e)}
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
            message=InsertDBFailed.message,
            extra={"exception": str(e)}
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


@blueprint.route('/list', methods=["GET"])
@jwt_required
@admin_required
def list():
    log_action = 'LIST_ROLES'
    member = Member.current_member()
    try:
        roles = Role.query.all()
        application_info_logger(
            200,
            message='Roles Returned Successfully',
            action=log_action,
            username=member.email,
        )
        schema = RoleSchema(many=True).dump(roles)
        return jsonify(schema), 200

    except Exception as e:
        application_error_logger(
            FetchDataException.status_code,
            action=log_action,
            username=member.email,
            message=FetchDataException.message,
            extra={"exception": str(e)}
        )
        raise FetchDataException.message


@blueprint.route('/get/<id>', methods=['GET'])
@jwt_required
@admin_required
def get(id):
    log_action = 'GET_ROLE'
    member = Member.current_member()
    valid_id = uuid_validator(id)
    try:
        role = Role.query.get_or_404(valid_id)
        if not role:
            application_error_logger(
                RoleNotFound.status_code,
                action=log_action,
                username=member.email,
                message=RoleNotFound.message,
            )
            raise RoleNotFound

        application_info_logger(
            200,
            message='Role Returned Successfully',
            action=log_action,
            username=member.email,
            extra={"role": str(role.title)}
        )
        schema = RoleSchema()
        return jsonify(schema.dump(role)), 200

    except Exception as e:
        application_error_logger(
            FetchDataException.status_code,
            action=log_action,
            username=member.email,
            message=FetchDataException.message,
            extra={"exception": str(e)}
        )
        raise FetchDataException
