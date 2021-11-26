from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from werkzeug.security import generate_password_hash

from application.mixin import SoftDeleteMixin
from application.extensions import db, ma


class Member(db.Model, SoftDeleteMixin):
    __tablename__ = 'member'

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, nullable=True)
    add_to_room = db.Column(db.Boolean, default=True)
    removed_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # Unique constraint on email
    __table_args__ = (
        db.UniqueConstraint('email', name='_account_email_unique'),
    )

    def __init__(self, email, hashed_password, fullname):
        self.email = email
        self.hashed_password = hashed_password
        self.fullname = fullname

    @classmethod
    def hash_password(cls, password):
        return generate_password_hash(password)

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            fullname=self.fullname,
            created_at=self.created_at,
            removed_at=self.removed_at,
            is_deleted=self.is_deleted,
            add_to_room=self.add_to_room,
        )


class MemberSchema(ma.SQLAlchemyAutoSchema):
    is_deleted = ma.Method('get_member_status')

    class Meta:
        model = Member
        exclude = ['hashed_password']

    def get_member_status(self, obj):
        status = True if obj.removed_at else False
        return status

