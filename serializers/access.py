from marshmallow import Schema, fields, validate


class AccessSerializer(Schema):
    title = fields.String(required=True, validate=validate.Length(min=0, max=50))
