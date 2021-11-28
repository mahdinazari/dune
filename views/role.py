from flask import Blueprint,request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required

from application.extensions import db
from models.member import Member, MemberSchema
from models.role import Role
from application.exceptions import FormDataNotValid, DuplicateRoleFound


blueprint = Blueprint('role', __name__, url_prefix='/api/v1/role')


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

