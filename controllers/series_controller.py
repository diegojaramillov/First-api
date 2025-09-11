# controllers/series_controller.py
# Aquí definimos los endpoints (rutas HTTP). Usamos un Blueprint para agruparlas.

from flask import Blueprint, jsonify, request

from services.series_service import (
    get_all, get_by_id, create_series,
    update_series, delete_series, title_exists,
    stats_by_platform
)

series_bp = Blueprint('series', __name__)

@series_bp.route('/series', methods=['GET'])
def route_get_all():
    """GET /series -> devuelve la lista completa de series"""
    return jsonify(get_all()), 200

@series_bp.route('/series/<int:series_id>', methods=['GET'])
def route_get_by_id(series_id):
    """GET /series/<id> -> devuelve una serie por id"""
    s = get_by_id(series_id)
    if s is None:
        return jsonify({"error": "Serie no encontrada"}), 404
    return jsonify(s), 200

@series_bp.route('/series', methods=['POST'])
def route_create_series():
    """
    POST /series
    Crea una nueva serie.
    Requiere JSON con 'title' (obligatorio).
    """
    if not request.is_json:
        return jsonify({"error": "Se esperaba JSON en el body"}), 400
    data = request.get_json()

    # Validaciones básicas
    if 'title' not in data or not isinstance(data['title'], str) or not data['title'].strip():
        return jsonify({"error": "Falta 'title' o no es válido"}), 400
    if 'seasons' in data:
        try:
            seasons = int(data['seasons'])
            if seasons < 1:
                return jsonify({"error": "'seasons' debe ser >= 1"}), 400
        except:
            return jsonify({"error": "'seasons' debe ser un número entero"}), 400

    # Comprobar título único (evita duplicados)
    if title_exists(data['title']):
        return jsonify({"error": "Ya existe una serie con ese título"}), 400

    new = create_series(data)
    return jsonify(new), 201

@series_bp.route('/series/<int:series_id>', methods=['PUT'])
def route_update_series(series_id):
    """
    PUT /series/<id>
    Actualiza una serie existente. Body: JSON con los campos a actualizar.
    """
    if not request.is_json:
        return jsonify({"error": "Se esperaba JSON en el body"}), 400
    data = request.get_json()

    # Si envían seasons validar
    if 'seasons' in data:
        try:
            seasons = int(data['seasons'])
            if seasons < 1:
                return jsonify({"error": "'seasons' debe ser >= 1"}), 400
        except:
            return jsonify({"error": "'seasons' debe ser un número entero"}), 400

    updated = update_series(series_id, data)
    if updated is None:
        return jsonify({"error": "Serie no encontrada"}), 404
    return jsonify(updated), 200

@series_bp.route('/series/<int:series_id>', methods=['DELETE'])
def route_delete_series(series_id):
    """DELETE /series/<id> -> elimina una serie"""
    deleted = delete_series(series_id)
    if not deleted:
        return jsonify({"error": "Serie no encontrada"}), 404
    return jsonify({"result": "Serie eliminada"}), 200

@series_bp.route('/series/stats', methods=['GET'])
def route_stats():
    """GET /series/stats -> devuelve estadísticas (conteo por plataforma)"""
    return jsonify(stats_by_platform()), 200
