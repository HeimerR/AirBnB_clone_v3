#!/usr/bin/python3
""" init get methods """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ returns if the app is working """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ return number of instances """
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        })
