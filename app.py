from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Registrar blueprints
    from controllers.auth_controller import auth_bp
    from controllers.series_controller import series_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(series_bp, url_prefix='/series')

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
