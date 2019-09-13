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


@app_views.route('/places_search', methods=['POST'])
def place_search():
    """ POST method to search a place bases in json body"""
    if not request.is_json:
        abort(400, "Not a JSON")
    parms = request.get_json()
    vals = [len(item) for item in parms.values()]
    if ((len(parms) is 0) or (max(vals) is 0)):
        places = storage.all("Place").values()
        return jsonify([item.to_dict() for item in places])
    places = []
    places_ids = []
    if 'states' in parms and len(parms.get('states')) > 0:
        states = parms.get('states')
        states_obj = [storage.get('State', state) for state in states]
        for state_obj in states_obj:
            state_cities = state_obj.cities
            for city in state_cities:
                city_places = city.places
                for place in city_places:
                    places.append(place.to_dict())
    if 'cities' in parms and len(parms.get('cities')) > 0:
        cities = parms.get('cities')
        cities_obj = [storage.get('City', city) for city in cities]
        for city in cities_obj:
            city_places = city.places
            for place in city_places:
                places.append(place.to_dict())
    if 'amenities' in parms and len(parms.get('amenities')) > 0:
        amenities = parms.get('amenities')
        amenities_obj = [storage.get('Amenity', amenity)
                         for amenity in amenities]
        places_obj = storage.all('Place').values()
        for place in places_obj:
            amenity_place = []
            amenities2 = place.amenities
            for amenity2 in amenities2:
                amenity_place.append(amenity2.id)
            for amenity in amenities:
                if amenity in amenity_place:
                    flag = True
                else:
                    flag = False
                    break
            if flag is True:
                place2 = place.to_dict()
                del place2['amenities']
                places.append(place2)
    places = [i for n, i in enumerate(places) if i not in places[n + 1:]]
    return jsonify(places)
