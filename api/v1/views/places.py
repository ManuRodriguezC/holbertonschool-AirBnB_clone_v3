#!/usr/bin/python3
"""This module create API of the places"""
from models import storage
from flask import request, make_response, jsonify
from models.place import Place
from models.city import City
from api.v1.views import app_views

met = ['GET', 'DELETE', 'POST', 'PUT']
list_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']


@app_views.route('/cities/<city_id>/places', methods=met, strict_slashes=False)
def places(city_id=None):
    """Method that give city id for return all places"""
    if request.method == 'GET':
        if city_id:
            city = storage.get(City, city_id)
            if city:
                cities = [places.to_dict() for places in city.places]
                return jsonify(cities)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'POST':
        content = request.get_json()
        if content:
            if "name" not in content:
                    return make_response(jsonify({"error": "Missing name"}), 400)
            if "user_id" not in content:
                    return make_response(jsonify({"error": "Missing user_id"}), 400)
            if city_id:
                city = storage.get(City, city_id)
                if city:
                    new = Place(**content)
                    new.save()
                    return make_response(jsonify(new.to_dict()), 200)
                return make_response(jsonify({"error": "Not found"}), 404)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/places/<place_id>', methods=met, strict_slashes=False)
def place_id(place_id=None):
    """Method that give place id"""
    if request.method == 'GET':
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                return make_response(jsonify(place.to_dict()), 200)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'DELETE':
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                storage.delete(place)
                storage.save()
                return make_response(jsonify({}), 200)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'PUT':
        content = request.get_json()
        if not content:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if place_id:
            place = storage.get(Place, place_id)
            if not place:
                return make_response(jsonify({"error": "Not found"}), 404)
            for key, value in content.items():
                if key not in list_keys:
                    setattr(place, key, value)
                    place. save()
                    return make_response(jsonify(place.to_dict()), 200)
            return make_response(jsonify({"error": "Not found"}), 404)
