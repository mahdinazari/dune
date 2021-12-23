from functools import wraps

from application.exceptions import AuthorizationError
from models.member import Member
from models.role import Role


def admin_required(fn):
    """
    A decorator for check is admin or not.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        member = Member.current_member()
        role = Role.query.get(member.role.id)
        if not role:
            raise AuthorizationError

        if not role.title == 'admin':
            raise AuthorizationError

        return fn(*args, **kwargs)

    return wrapper
