from flask_script import Manager
from flask_migrate import MigrateCommand

from application.app import create_app
from application.extensions import db
from models.member import Member


app = create_app('application.config.Config')
manager = Manager(app)


@manager.command
def create_db():
    """
    Create Database
    """
    db.create_all()


@manager.command
def drop_db():
    """
    Drop Database
    """
    db.drop_all()


@manager.command
def create_member(email, password, fullname):
    hashed_password = Member.hash_password(password)
    member = Member(email, hashed_password, fullname)
    duplicate_member = Member.query \
        .filter(Member.email == member.email) \
        .first()

    if duplicate_member:
        return "Member Already Exists"

    try:
        db.session.add(member)
        db.session.commit()
        return "Member Has Been Added"

    except:
        return "Create Member Exception Occured"


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

