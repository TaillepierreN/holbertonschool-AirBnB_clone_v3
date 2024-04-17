#!/usr/bin/python3
"""View fo city objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
        return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city ibject and return rais error 404 if not linked"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    city.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    new_city = request.get_json()
    if new_city is None:
        abort(404, 'Not a JSON')
    if "name" not in new_city:
        abort(404, 'Missing name')
    new_city['state_id'] = state_id
    city = City(**city)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    updated_city = request.get_json()
    if updated_city is None:
        abort(404, 'Not a JSON')
        for key, value in updated_city.items():
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
