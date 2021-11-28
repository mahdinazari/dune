from marshmallow import Schema, fields, validate


class RoleSerializer(Schema):
    title = fields.String(validate=validate.Length(min=3, max=50))
