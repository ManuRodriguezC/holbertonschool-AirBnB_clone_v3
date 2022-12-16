#!/usr/bin/python
"""
"""
from models import storage
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, make_response

list_met = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/users', methods=list_met, strict_slashes=False)
@app_views.route('/users/<user_id>', methods=list_met, strict_slashes=False)
def states(user_id=None):
    """
    """
    if request.method == 'GET':
        if user_id:
            obj = storage.get(User, user_id)
            if obj:
                return jsonify(obj.to_dict())
            return make_response(jsonify({'error': 'Not found'}), 404)
        user_objs = [state.to_dict() for state in storage.all(User).values()]
        return jsonify(user_objs)

    if request.method == 'DELETE':
        if user_id:
            obj = storage.get(User, user_id)
            if obj:
                storage.delete(obj)
                storage.save()
                return make_response(jsonify({}), 200)
            return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'POST':
        content = request.get_json()
        if content:
            if "email" not in content:
                return make_response(jsonify("error"": Missing email"), 400)
            if "password" not in content:
                return make_response(jsonify("error"": Missing password"), 400)
            else:
                new = User(**content)
                new.save()
                return make_response(jsonify(new.to_dict()), 201)
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if request.method == 'PUT':
        if user_id:
            content = request.get_json()
            if not content:
                return make_response(jsonify({"error": "Not a JSON"}), 400)
            user = storage.get(User, user_id)
            if not user:
                return make_response(jsonify({"error": "Not found"}), 404)
            for key, value in content.items():
                if key != "id" and key != "email" and key != "created_at" and key != "updated_at":
                    setattr(user, key, value)
                    user.save()
                    return make_response(jsonify(user.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
