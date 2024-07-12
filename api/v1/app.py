#!/usr/bin/python3
"""This module defines a flask web app"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """This method handles the teardown, on itself"""
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """ return for 404 errors """
    return jsonify({"error": "Not found"}), 404


def start_flask():
    """
    starts flask - sets host and port from getenv
    if 'name == main' runs this method
    """
    app.run(host=getenv('HBNB_API_HOST', default='localhost'),
            port=getenv('HBNB_API_PORT'),
            threaded=True, debug=True)


if __name__ == "__main__":
    start_flask()
