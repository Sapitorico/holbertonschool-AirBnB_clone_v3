#!/usr/bin/python3
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, make_response, request

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def  get_cities(state_id):
    """return a list of cities"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

# @app_views.route('/cities', methods=['GET'])
# def get_states2():
#     """Return a list of all states"""
#     states = storage.all(City).values()
#     state_list = [state.to_dict() for state in states]
#     return jsonify(state_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities_by_city_id(city_id):
    """return a city object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    storage.delete(city)
    storage.reload()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    request_data['state_id'] = state_id
    new_city = City(**request_data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
