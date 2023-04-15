#!/usr/bin/python3
"""http methods for manipulating sate class resources"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, make_response, request


@app_views.route('/amenities/', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Return a list of all amenity"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Return a amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
