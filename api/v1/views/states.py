#!/usr/bin/python3
"""http methods for manipulating sate class resources"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, make_response, request


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/', methods=['GET'])
def get_states():
    """Return a list of all states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Return a state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    storage.delete(state)
    storage.reload()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a new state"""
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
