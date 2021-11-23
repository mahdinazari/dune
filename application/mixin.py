from datetime import datetime

from application.app import db


class SoftDeleteMixin:
    removed_at = db.Column(
        db.DateTime,
        default=None,
        nullable=True,
    )

    def assert_is_not_deleted(self):
        if self.is_deleted:
            raise ValueError('Object is already deleted.')

    def assert_is_deleted(self):
        if not self.is_deleted:
            raise ValueError('Object is not deleted.')

    @property
    def is_deleted(self):
        return True if self.removed_at is not None else False

    def soft_delete(self, ignore_errors=False):
        if not ignore_errors:
            self.assert_is_not_deleted()
        self.removed_at = datetime.utcnow()
        