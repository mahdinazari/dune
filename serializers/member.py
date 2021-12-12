from uuid import uuid4
from datetime import datetime

from marshmallow import Schema, fields, validate

from application.config import Config


class MemberSerializer(Schema):
    # pattern = r"^[0-9]"
    # ip = fields.String(validate=validate.Regexp(pattern), required=True)
    # id = fields.UUID(attribute="id")
    
    min = Config.MIN_PASSWORD_LENGTH
    max = Config.MAX_PASSWORD_LENGTH

    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=min, max=max))
    fullname = fields.String(required=True)
    add_to_room = fields.Boolean(default=True)
    removed_at = fields.DateTime(default=None)
    created_at = fields.DateTime(default=datetime.now())


class LoginMemberSerializer(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
