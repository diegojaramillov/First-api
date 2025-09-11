# app.py
# Punto de entrada de la aplicación Flask.
# Registra los controladores y arranca el servidor.

from flask import Flask
from controllers.series_controller import series_bp

def create_app():
    # Crear instancia de Flask
    app = Flask(__name__)
    # Registrar blueprint que contiene todas las rutas de "series"
    app.register_blueprint(series_bp)
    return app

if __name__ == '__main__':
    # Si ejecutas python app.py, crea la app y la corre en debug
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
