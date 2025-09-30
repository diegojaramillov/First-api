from app import create_app
from repositories.user_repository import UserRepository

app = create_app()

with app.app_context():
    username = 'admin'
    password = 'admin123'  # Cámbiala luego
    if UserRepository.find_by_username(username):
        print('Admin ya existe.')
    else:
        admin = UserRepository.create_user(username, password, role='admin')
        print('Admin creado ->', admin.username)
        print('Recuerda cambiar la contraseña por seguridad.')
