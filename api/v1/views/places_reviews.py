#!/usr/bin/python3
"""
This module creates the view for all review objects
and handles all default api actions
"""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    This method retrieves a list of all reviews for a place
    Args: place - contains a place object
          reviews - holds reviews from a place
          reviews_list - dictionary of reviews linked to a place
    Return: a list of dictionaries containing reviews
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_reviews(review_id):
    """
    This method retrieves a review
    Args: review - contains one review object, based on its id
          reviews_json - dictionary holding review
    Return: dictionary holding review in json format
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_json = review.to_dict()
    return jsonify(review_json)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    This method deletes a review
    Args: review - contains one review object, based on its id
    Return: empty dictionary in json format
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    This method creates a review
    Args: review - contains one review object, based on its id
          user - contains user
    Return: empty dictionary in json format
    """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON') # Bad request
    place = storage.get(Place, place_id)
    if not place:
        abort(404) # Bad request
    if "user_id" not in json_data.keys():
        abort(400, "Missing user_id") # Bad request
    user = storage.get(User, json_data.get("user_id"))
    if not user:
        abort(404) # Bad request
    if "text" not in json_data.keys():
        abort(400, "Missing text")
    json_data["place_id"] = place_id
    review = Review(**json_data)
    review_json = review.to_dict()
    return jsonify(review_json), 201 # OK
