#!/usr/bin/python3
"""API Routes for Place Reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("places/<place_id>/reviews",
                 strict_slashes=False, methods=["GET"])
def get_reviews(place_id):
    """Retrieve all reviews for a place    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())

    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """Retrieve a specific review by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """Delete a review by ID """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["POST"])
def new_review(place_id):
    """Create a new review for a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data['place_id'] = place_id
    new_reviews = Review(**data)
    new_reviews.save()

    return jsonify(new_reviews.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """Update an existing review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")

    for key, value in review_data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()

    return jsonify(review.to_dict())
