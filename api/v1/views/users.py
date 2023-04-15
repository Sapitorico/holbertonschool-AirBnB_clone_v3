#!/usr/bin/python3
"""http methods for manipulating sate class resources"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """Return a list of all users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Return a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request_data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request_data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update user"""
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
