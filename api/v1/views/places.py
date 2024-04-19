#!/usr/bin/python3
"""View for the places"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """Retrieves all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())

    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object with a specific id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object with a specific id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def new_place(city_id):
    """Creates a Place object"""
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if "user_id" not in place_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, place_data.get("user_id"))
    if not user:
        abort(404)
    if "name" not in place_data.keys():
        abort(400, "Missing name")

    place_data["city_id"] = city_id
    place = Place(**place_data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object with a specific id"""
    place_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")

    for key, value in place_data.items():
        if key not in ["id", "state_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
