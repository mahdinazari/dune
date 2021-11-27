from flask import Blueprint, request, jsonify

from models.access import Access
from application.extensions import db
from utils import request_validator
from application.exceptions import EmptyForm, FormDataNotValid, DuplicateAccess, InsertDBFailed


blueprint = Blueprint('role', __name__, url_prefix='/api/v1/access')


@blueprint.route('/create', methods=['POST'])
def create():
    if not request.json:
        raise EmptyForm

    try:
        data = request.json

    except Exception as e:
        raise FormDataNotValid

    is_valid = request_validator('AccessSerializer', data)
    if not is_valid:
        raise FormDataNotValid

    try:
        title = data.get('title')
        access = Access(title)
        duplicate_member = Access.query \
            .filter(Access.title == access.email) \
            .first()
        if duplicate_member:
            raise DuplicateAccess

    except Exception as e:
        return jsonify("Register Exception"), 400

    try:
        db.session.add(access)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise InsertDBFailed

    return jsonify("Member Has Been Registered Successfully"), 200
