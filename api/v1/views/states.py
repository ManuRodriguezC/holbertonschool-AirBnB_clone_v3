#!/usr/bin/python3
""""""
from models import storage
from api.v1.views import app_views
from models.state import State
from flask import request, jsonify, make_response


list_methods = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/states', methods=list_methods, strict_slashes=False)
@app_views.route('/states/<state_id>', methods=list_methods, strict_slashes=False)
def states(state_id=None):
    """"""
    if request.method == 'GET':
        if state_id:
            obj = storage.get(State, state_id)
            if obj:
                return jsonify(obj.to_dict())
            return make_response(jsonify({'error': 'Not found'}), 404)
        state_objs = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(state_objs)

    if request.method == 'DELETE':
        if state_id:
            obj = storage.get(State, state_id)
            if obj:
                storage.delete(obj)
                storage.save()
                return make_response(jsonify({}), 200)
            return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'POST':
        content = request.get_json()
        if content:
            if "name" not in content:
                return make_response(jsonify("error"": Missing name"), 400)
            else:
                new = State(**content)
                new.save()
                return make_response(jsonify(new.to_dict()), 200)
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    """
    if request.method == 'PUT':
        content = request.get_json()
        if not content:
            return make_response(jsonify({"error"}))
        state = storage.get(State, state_id)
        
        if content:
            dates = storage.all()
            dates[]
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    """