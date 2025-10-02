from flask import Blueprint, request, jsonify
from services.series_service import SeriesService
from services.role_service import roles_required
from repositories.series_repository import SeriesRepository

series_bp = Blueprint('series', __name__)

@series_bp.route('/', methods=['GET'])
def list_series():
    items = SeriesService.list_series()
    return jsonify([s.to_dict() for s in items]), 200

@series_bp.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    s = SeriesService.get_series(series_id)
    if not s:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(s.to_dict()), 200

@series_bp.route('/', methods=['POST'])
@roles_required('admin')
def create_series():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'message': 'title is required'}), 400
    s = SeriesService.create_series(data)
    return jsonify(s.to_dict()), 201

@series_bp.route('/<int:series_id>', methods=['PUT'])
@roles_required('admin')
def update_series(series_id):
    s = SeriesService.get_series(series_id)
    if not s:
        return jsonify({'message': 'Not found'}), 404
    data = request.get_json() or {}
    s = SeriesService.update_series(s, data)
    return jsonify(s.to_dict()), 200

@series_bp.route('/<int:series_id>', methods=['DELETE'])
@roles_required('admin')
def delete_series(series_id):
    s = SeriesService.get_series(series_id)
    if not s:
        return jsonify({'message': 'Not found'}), 404
    SeriesService.delete_series(s)
    return jsonify({'message': 'Deleted'}), 200
