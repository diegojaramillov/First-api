import os
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, bcrypt, jwt


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    
    from controllers.auth_controller import auth_bp
    from controllers.series_controller import series_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(series_bp, url_prefix='/series')

    
    with app.app_context():
        db.create_all()

    return app
    
if __name__ == '__main__':
    app = create_app()
    # Allow disabling debug/reloader via environment variable DEBUG=1
    debug_flag = os.environ.get('DEBUG', '0') == '1'
    app.run(debug=debug_flag, host="0.0.0.0", port=5000, use_reloader=debug_flag)
