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