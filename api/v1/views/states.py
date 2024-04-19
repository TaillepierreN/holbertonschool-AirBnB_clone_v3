#!/usr/bin/python3
"""Script for the states view"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Method that retrieves the list of all State objects"""
    st = storage.all(State).values()
    states_list = []
    for state in st:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Method that retrieves a State object with a specific id"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    return jsonify(st.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Method that deletes a State object with a specific id"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    storage.delete(st)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def new_state():
    """Method that creates a State object"""
    st_data = request.get_json()
    if not st_data:
        abort(400, "Not a JSON")
    elif "name" not in st_data:
        abort(400, "Missing name")
    new_state = State(**st_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def change_state(state_id):
    """Method that updates a State object with a specific id"""
    st_data = request.get_json()
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    elif not st_data:
        abort(400, "Not a JSON")
    for key, value in st_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(st, key, value)
    storage.save()
    return jsonify(st.to_dict()), 200