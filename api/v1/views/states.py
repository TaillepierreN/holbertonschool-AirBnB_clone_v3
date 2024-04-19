#!/usr/bin/python3
"""view of State objects as RESTful API"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State"""
    all_state = storage.all(State).values()
    states_list = []
    for state in all_state:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object with a specific id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object with a specific id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def new_state():
    """Creates a State object"""
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    elif "name" not in state_data:
        abort(400, "Missing name")
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def change_state(state_id):
    """Updates a State object with a specific id"""
    state_data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not state_data:
        abort(400, "Not a JSON")
    for key, value in state_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
