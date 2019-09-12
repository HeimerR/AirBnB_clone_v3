#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities')
def amenities_from_place(place_id=None):
    """ GET amenities from place """
    amenities = []
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def amenity_review_delete(place_id=None, amenity_id=None):
    """ DELETE amenities  methods """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        abort(404)
    if not amenity.id  in place.amenities.id:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def amenity_from_place_post(place_id):
    """ POST method to create a amenity """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        abort(404)
    if amenity.id  in place.amenities.id:
        return (jsonify(amenity.to_dict()), 200)
