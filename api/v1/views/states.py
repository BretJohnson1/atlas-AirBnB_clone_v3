#!/usr/bin/python3
"""
This module creates the view for all state objects
and handles all default api actions
"""

from api.v1.views import app_views, index
from flask import Flask, abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    This method retrieves a list of all state objects
    Args: states_all - list of all states, keys excluded
          states_json - all states converted to a list of dictionaries
    Return: a json dictionary containing all state objects
    """
    states_all = storage.all(State).values()
    # print(f"states_all type: {type(states_all)}")
    states_json = [state.to_dict() for state in states_all]
    return jsonify(states_json)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
    This method retrieves one state object
    Args: state - retrieves one state object, based on its state id
          state_json - state object converted to a dictionary
    Return: a json dictionary containing one state object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # Bad request
    state_json = state.to_dict()
    return jsonify(state_json)


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """
    This method deletes one state object
    Args: state - retrieves one state object, based on its state id
    Return: an empty json dictionary
    """
    # print("here")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # Bad request
    storage.delete(state)
    storage.save()
    return jsonify({}), 200  # OK
    # ^^^ not 200? -Ace
    # Nvm yeah I went ahead and changed it. -Ace


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    This method creates a state object
    Args: state - gets an HTTP body request to a state object
          json_data - holds the json data request
    Return: a json dictionary containing one state object
    """
    json_data = request.get_json(silent=True)
    if not json_data:
        # print("here")
        abort(400, "Not a JSON")  # Bad request
    if "name" not in json_data:
        abort(400, "Missing name")  # Bad request
    state = State(**json_data)
    state.save()
    state_json = state.to_dict()
    return jsonify(state_json), 201  # OK


@app_views.route(
        "/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    This method updates a state object
    Args: state - retrieves one state object, based on its state id
          json_data - json request data for readability
          state_json - state object converted to a dictionary
    Return:
    """
    state = storage.get(State, state_id)
    json_data = request.get_json(silent=True)
    if not state:
        abort(404)  # Bad request
    if not json_data:
        abort(400, "Not a JSON")  # Bad request
    if "name" not in json_data:
        abort(400, "Missing name")  # Bad request
    for key, value in json_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    state_json = state.to_dict()
    return jsonify(state_json)
