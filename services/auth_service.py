from repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token

class AuthService:

    @staticmethod
    def register(username, password, role='user'):
        if UserRepository.find_by_username(username):
            return {'message': 'User already exists'}, 400

        user = UserRepository.create_user(username, password, role)
        return {'message': 'User created', 'user': user.to_dict()}, 201

    @staticmethod
    def login(username, password):
        user = UserRepository.find_by_username(username)
        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        # guardamos role en additional_claims para acceder fácil desde get_jwt()
        additional_claims = {'role': user.role, 'username': user.username}
        # Use string identity to ensure JWT 'sub' claim is a string (some JWT libraries require this)
        token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        return {'access_token': token, 'user': user.to_dict()}, 200
