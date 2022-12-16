#!/usr/bin/python3
"""This module create API for cities"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import make_response, jsonify, request

met = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('states/<state_id>/cities', methods=met, strict_slashes=False)
def cities(state_id=None):
    """Take te cities in the speficic state"""
    if request.method == "GET":
        if state_id:
            state = storage.get(State, state_id)
            if state:
                state_objs = [city.to_dict() for city in state.cities]
                return jsonify(state_objs)
            return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'POST':
        content = request.get_json()
        if content:
            if "name" not in content:
                return make_response(jsonify("error"": Missing name"), 400)
            state = storage.get(State, state_id)
            if state:
                content["state_id"] = state_id
                new = City(**content)
                new.save()
                return make_response(jsonify(new.to_dict()), 200)
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/cities/<city_id>', methods=met, strict_slashes=False)
def city(city_id=None):
    """This method take a anycity"""
    if request.method == 'GET':
        if city_id:
            city_current = storage.get(City, city_id)
            if city_current:
                return jsonify(city_current.to_dict())
            return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'DELETE':
        if city_id:
            city_current = storage.get(City, city_id)
            if city_current:
                storage.delete(city_current)
                storage.save()
                return make_response(jsonify({}), 200)
            return make_response(jsonify({"error": "Not found"}))

    if request.method == 'PUT':
        if city_id:
            content = request.get_json()
            if not content:
                return make_response(jsonify({"error": "Not a JSON"}), 400)
            city_current = storage.get(City, city_id)
            if not city_current:
                return make_response(jsonify({"error": "Not found"}), 404)
            for key, value in content.items():
                setattr(city_current, key, value)
                city_current.save()
                return make_response(jsonify(city_current.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
