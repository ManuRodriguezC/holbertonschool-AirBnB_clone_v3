#!/usr/bin/python3
""""""
from models import storage
from api.v1.views import app_views
from models.state import State
from api.v1.app import not_found
import requests


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """"""
    if state_id:
        obj = storage.get(State, state_id)
        if obj:
            return obj.to_dict()
        return not_found(404) 
    state_objs = [state.to_dict() for state in storage.all(State).values()]
    return state_objs

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def states_del(state_id=None):
    """"""
    if state_id:
        obj = storage.get(State, state_id)
        if obj:
            objeto = "State.{}".format(state_id)
            storage.delete(objeto)
            storage.save()
            return {}
        return not_found(404)
