from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.mixin import SoftDeleteMixin


class Role(db.Model, SoftDeleteMixin):
    __tablename__ = 'role'

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    removed_at = db.Column(db.DateTime, default=None)
    updated_at = db.Column(db.DateTime, default=datetime.now())

    accesses = db.relationship("Access", backref="role", lazy='dynamic')
    