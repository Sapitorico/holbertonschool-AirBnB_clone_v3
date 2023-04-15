#!/usr/bin/python3
"""http methods for manipulating sate class resources"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """return a list of review"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    review_list = [review.to_dict() for review in place.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """return a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, request_data['user_id'])
    if user is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if 'text' not in request_data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    request_data['place_id'] = place_id
    new_review = Review(**request_data)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a city"""
    review = storage.get(Review, review_id)
    if review is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
