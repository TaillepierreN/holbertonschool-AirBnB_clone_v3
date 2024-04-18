#!/usr/bin/python3
"""Create a view for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import base_model
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves list of all Amenities objects"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())

    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ create a new amenity object """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, 'Not a JSON')

    if 'name' not in new_amenity:
        abort(400, 'Missing name')

    amenity = Amenity(**new_amenity)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    up_amenity = request.get_json()
    if up_amenity is None:
        abort(400, 'Not a JSON')
    for key, value in up_amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
