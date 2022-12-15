#!/usr/bin/python3
"""This module created the routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review,
           "States": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """This route return a json"""
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """This method return the numbers of the objects"""
    number_objects = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(number_objects)
