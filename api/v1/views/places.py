#!/usr/bin/python3
"""http methods for manipulating sate class resources"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    """Return a list of all places for a given city"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """return a city object"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Delete a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new place for city"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    request_data['city_id'] = city_id
    new_place = Place(**request_data)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place in the database"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
