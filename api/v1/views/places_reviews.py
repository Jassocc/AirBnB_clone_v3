#!/usr/bin/python3
"""
Reviews view module
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrieves the list of all reveiw objects of a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = storage.all(Review).values()
    place_reviews = [review.to_dict() for review in reviews
                     if review.place_id == place_id]
    return jsonify(place_reviews)


@app_reviews.route('/reviews/<review_id>', methods=['GET'],
                   strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a review object by review_id
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by review_id
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review in a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    data["place_id"] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object by review_id
    """
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ["id", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(review, key, value)

        storage.save()
        return jsonify(review.to_dict()), 200

    abort(404)
