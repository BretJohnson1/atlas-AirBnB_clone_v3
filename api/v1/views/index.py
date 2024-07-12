#!/usr/bin/python3
"""The module conatins the index for the api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# Here's a dictionary of classes for future use
classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_stats():
    """returns counts of the different objects"""
    return_dict = {}
    for object in classes:
        # print({object})
        object_dict = {object: storage.count(classes[object])}
        return_dict.update(object_dict)
    return jsonify(return_dict)
