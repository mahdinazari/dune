from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.mixin import SoftDeleteMixin
from application.extensions import db, ma
from models.role import RoleSchema


class Member(db.Model, SoftDeleteMixin):
    __tablename__ = 'member'

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, nullable=True)
    add_to_room = db.Column(db.Boolean, default=True)
    removed_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())

    role = db.relationship('Role')
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'))

    # Unique constraint on email
    __table_args__ = (
        db.UniqueConstraint('email', name='_account_email_unique'),
    )

    def __init__(self, email, hashed_password, fullname):
        self.email = email
        self.hashed_password = hashed_password
        self.fullname = fullname

    @property
    def member_role(self):
        return None if self.role is None else self.role.title

    @classmethod
    def hash_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        member = cls.query.filter_by(email=email).first()
        if not member or not check_password_hash(member.password, password):
            return None

        return member

    @classmethod
    @jwt_required
    def current_member(cls):
        with current_app.test_request_context():
            member = Member.query.get(get_jwt_identity()['id'])
            if not member:
                return jsonify(message="401 Invalid credentials"), 401

        return member

    @classmethod
    @jwt_required
    def check_duplicate_email(cls, email):
        email = Member.query \
            .filter_by(email=email) \
            .one_or_none()
        return True if email is not None else None

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            fullname=self.fullname,
            role_id=self.role_id,
            role=self.role,
            created_at=self.created_at,
            removed_at=self.removed_at,
            is_deleted=self.is_deleted,
            add_to_room=self.add_to_room,
        )


class MemberSchema(ma.SQLAlchemyAutoSchema):
    is_deleted = ma.Method('get_member_status')
    role = ma.Nested('RoleSchema',  only=['id', 'title'])

    class Meta:
        model = Member
        exclude = ['hashed_password']

    def get_member_status(self, obj):
        status = True if obj.removed_at else False
        return status
