#!/usr/bin/python3
"""
This module creates the view for all city objects
and handles all default api actions
"""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
        "/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """
    This method retrieves a list of all cities in one state
    Args: cities - contains a list all cities in one state
          state - contains one state object
    Return: a list dictionaries with cities and
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route(
        "/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    This method retrieves one city object
    Args: city - contains one city object, based on its city id
          city_json - city object converted to a dictionary
    Return: a json dictionary containing one city object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)  # Bad request
    city_json = city.to_dict()
    return jsonify(city_json)


@app_views.route(
        "/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    This method deletes a city object
    Args: city - contains one city object, based on its city id
    Return: an empty dictionary
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)  # Bad request
    storage.delete(city)
    storage.save()
    return jsonify({}), 200  # OK


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    This method creates a city object
    Args: state - contains a state object
          city - contains an HTTP body request to a city object
          json_data - holds the json data request
          city_json - holds the dictionary representation of city
    Return:
    """
    state = storage.get(State, state_id)
    json_data = request.get_json(silent=True)
    if not json_data:
        print("here")
        abort(400, "Not a JSON")  # Bad request
    if "name" not in json_data:
        abort(400, "Missing name")  # Bad request
    if not state:
        abort(404)

    city = City(**json_data)
    setattr(city, "state_id", state_id)
    city.save()
    city_json = city.to_dict()
    return jsonify(city_json), 201  # OK


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    This method updates a city object
    Args: json_data - holds the json data request
          city - contains one city object
          city_json - holds the dictionary representation
    Return:
    """
    json_data = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not json_data:
        abort(400, "Not a JSON")
    for key, value in json_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    city_json = city.to_dict()
    return jsonify(city_json)
