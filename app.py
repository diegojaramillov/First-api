# ================================
# 📌 Importación de librerías
# ================================
from flask import Flask, jsonify, request

# ================================
# 📌 Configuración de la app Flask
# ================================
app = Flask(__name__)  # Creamos la instancia de Flask

# ================================
# 📌 Datos simulados (base de datos en memoria)
# ================================
# Lista de series de comedia, cada una es un diccionario con su información
comedy_series = [
    {
        "id": 1,
        "title": "Shameless",
        "seasons": 11,
        "platform": "Netflix"
    },
    {
        "id": 2,
        "title": "Brooklyn Nine-Nine",
        "seasons": 8,
        "platform": "Peacock"
    }
]

# ================================
# 📌 Rutas de la API (Endpoints)
# ================================

# 1️⃣ Obtener todas las series
@app.route('/series', methods=['GET'])
def get_all_series():
    """
    Devuelve la lista completa de series en formato JSON
    """
    return jsonify(comedy_series), 200


# 2️⃣ Obtener una serie por su ID
@app.route('/series/<int:series_id>', methods=['GET'])
def get_series(series_id):
    """
    Busca una serie por su ID y la devuelve.
    Si no existe, devuelve un error 404.
    """
    series = next((s for s in comedy_series if s['id'] == series_id), None)
    if series is None:
        return jsonify({"error": "Serie no encontrada"}), 404
    return jsonify(series), 200


# 3️⃣ Crear una nueva serie
@app.route('/series', methods=['POST'])
def create_series():
    """
    Crea una nueva serie. 
    Espera un JSON con "title", "seasons" y "platform".
    """
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Solicitud inválida, falta 'title'"}), 400
    
    # Generamos un nuevo ID de forma automática
    new_id = max(s['id'] for s in comedy_series) + 1 if comedy_series else 1

    # Creamos el diccionario de la nueva serie
    new_series = {
        "id": new_id,
        "title": request.json['title'],
        "seasons": request.json.get('seasons', 1),  # Si no envían temporadas, asumimos 1
        "platform": request.json.get('platform', "Desconocida")
    }

    comedy_series.append(new_series)
    return jsonify(new_series), 201  # 201 = Created


# 4️⃣ Actualizar una serie existente
@app.route('/series/<int:series_id>', methods=['PUT'])
def update_series(series_id):
    """
    Actualiza los datos de una serie existente.
    """
    series = next((s for s in comedy_series if s['id'] == series_id), None)
    if series is None:
        return jsonify({"error": "Serie no encontrada"}), 404
    
    if not request.json:
        return jsonify({"error": "Solicitud inválida"}), 400
    
    # Actualizamos solo los campos enviados en el request
    series['title'] = request.json.get('title', series['title'])
    series['seasons'] = request.json.get('seasons', series['seasons'])
    series['platform'] = request.json.get('platform', series['platform'])
    
    return jsonify(series), 200


# 5️⃣ Eliminar una serie
@app.route('/series/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    """
    Elimina una serie por su ID.
    """
    series = next((s for s in comedy_series if s['id'] == series_id), None)
    if series is None:
        return jsonify({"error": "Serie no encontrada"}), 404
    
    comedy_series.remove(series)
    return jsonify({"result": "Serie eliminada"}), 200


# Buscar series por plataforma
@app.route('/series/platform/<string:platform>', methods=['GET'])
def get_series_by_platform(platform):
    result = [s for s in comedy_series if s['platform'].lower() == platform.lower()]
    return jsonify(result), 200


# ================================
# 📌 Ejecutar la app
# ================================
if __name__ == '__main__':
    # Ejecuta el servidor en modo debug y accesible en red local
    app.run(debug=True, host='0.0.0.0', port=5000)
