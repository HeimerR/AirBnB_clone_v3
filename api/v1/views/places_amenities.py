#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os
import sqlalchemy


db = os.environ.get('HBNB_TYPE_STORAGE', None)


@app_views.route('/places/<place_id>/amenities')
def amenities_from_place(place_id=None):
    """ GET amenities from place """
    amenities = []
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        if db is 'db':
            for amenity in place.amenities:
                amenities.append(amenity.to_dict())
            return jsonify(amenities)
        else:
            jsonnify(place.amenities())


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'])
def amenity_review_delete(place_id=None, amenity_id=None):
    """ DELETE amenities from a place methods """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        abort(404)
    if amenity.id not in place.amenities.id:
        abort(404)

    if db is 'db':
        place.amenities.remove(amenity)
        return (jsonify({}), 200)
    else:
        place.amenities().remove(amenity.id)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def amenity_from_place_post(place_id):
    """ POST method to create a amenity """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        abort(404)
    if amenity.id in place.amenities.id:
        return (jsonify(amenity.to_dict()), 200)
    if db is 'db':
        place.amenities.append(amenity)
        return (jsonify(amenity.to_dict()), 201)
