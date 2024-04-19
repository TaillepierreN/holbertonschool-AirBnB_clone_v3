#!/usr/bin/python3
"""Script for the places_reviews view"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_all_reviews(place_id):
    """Method that retrieves the list of all Review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Method that retrieves a Review object with a specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Method that deletes a Review object with a specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def new_review(place_id):
    """Method that creates a Review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def change_review(review_id):
    """Method that updates a Review object with a specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
