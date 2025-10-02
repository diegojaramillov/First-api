from models.user import User
from extensions import db

class UserRepository:

    @staticmethod
    def create_user(username, password, role='user'):
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)
