#!/usr/bin/python3
"""This module created API review"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import request, make_response, jsonify
from api.v1.views import app_views

met = ['GET', 'DELETE', 'POST', 'PUT']
list_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']


@app_views.route('/places/<place_id>/reviews', methods=met, strict_slashes=False)
def reviews(place_id=None):
    """This method give place id in reviews"""
    if request.method == 'GET':
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                review = [date.to_dict() for date in place.reviews]
                return jsonify(review)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'POST':
        content = request.get_json()
        if not content:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "text" not in content:
            return make_response(jsonify({"error": "Missing name"}), 400)
        if "user_id" not in content:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                user = storage.get(User, content['user_id'])
                if not user:
                    return make_response(jsonify({"error": "Not found"}), 404)
                content["place_id"] = place_id
                new = Review(**content)
                new.save()
                return make_response(jsonify(new.to_dict()), 201)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>', methods=met, strict_slashes=False)
def review(review_id=None):
    """This method return review with id"""
    if request.method == 'GET':
        if review_id:
            review = storage.get(Review, review_id)
            if review:
                return make_response(jsonify(review.to_dict()), 200)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review_id:
            if review:
                storage.delete(review)
                storage.save()
                return make_response(jsonify({}), 200)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)
        

    if request.method == 'PUT':
        content = request.get_json()
        if not content:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if review_id:
            review = storage.get(Review, review_id)
            if not review:
                return make_response(jsonify({"error": "Not found"}), 404)
            for key, value in content.items():
                if key not in list_keys:
                    setattr(review, key, value)
            review. save()
            return make_response(jsonify(review.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
