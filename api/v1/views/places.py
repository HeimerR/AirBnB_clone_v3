#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>')
def places(place_id=None):
    """ GET place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places')
def city_place(city_id=None):
    """ basic GET places by city method """
    places = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)


@app_views.route('places/<place_id>', methods=['DELETE', 'PUT'])
def place_delete(place_id=None):
    """ DELETE and PUT place methods """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        to_update = request.get_json()
        for key, value in to_update.items():
            if (key is not "id" and key is not "created_at" and
                    key is not "updated_at" and key is not "user_id" and
                    key is not "city_id"):
                setattr(place, key, value)
        place.save()
        return (jsonify(place.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """ POST method to create a place """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    new = request.get_json()
    user_id = new.get("user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_obj = Place(**new)
    setattr(new_obj, "city_id", city_id)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
