#!/usr/bin/python3
"""API Routes for Place Reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieve all reviews for a place"""
    place_from_id = storage.get(Place, place_id)
    if not place_from_id:
        abort(404)
    reviews = place_from_id.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_reviews(review_id):
    """Retrieve a specific review by ID"""
    review_from_id = storage.get(Review, review_id)
    if not review_from_id:
        abort(404)
    return jsonify(review_from_id.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review by ID"""
    review_from_id = storage.get(Review, review_id)
    if not review_from_id:
        abort(404)
    storage.delete(review_from_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def new_review(place_id):
    """Create a new review for a place"""
    review_from_id_data = request.get_json()
    if not review_from_id_data:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in review_from_id_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, review_from_id_data.get("user_id"))
    if not user:
        abort(404)
    if "text" not in review_from_id_data.keys():
        abort(400, "Missing text")

    review_from_id_data["place_id"] = place_id
    new_review = Review(**review_from_id_data)
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def change_review(review_id):
    """Update an existing review"""
    review_from_id_data = request.get_json()
    review_from_id = storage.get(Review, review_id)
    if not review_from_id:
        abort(404)
    elif not review_from_id_data:
        abort(400, "Not a JSON")

    for key, value in review_from_id_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review_from_id, key, value)
    storage.save()
    return jsonify(review_from_id.to_dict()), 200
