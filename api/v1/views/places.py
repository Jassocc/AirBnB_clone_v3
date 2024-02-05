#!/usr/bin/python3
"""
Places view module
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = storage.all(Place).values()
    city_places = [place.to_dict() for place in places
                   if place.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by place_id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by place_id
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place in a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by place_id
    """
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json()
        if not data:
            return jsonify({"error":
                            "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ["id", "user_id", "city_id",
                           "created_at", "updated_at"]:
                setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict()), 200

    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Search for places
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    states_ids = data.get("states", [])
    cities_ids = data.get("cities", [])
    amenities_ids = data.get("amenities", [])
    places_result = []
    if not states_ids and not cities_ids and not amenities_ids:
        places_result = [place.to_dict() for place in
                         storage.all(Place).values()]
    else:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                cities_ids.extend([city.id for city in state.cities])
        for city_id in set(cities_ids):
            city = storage.get(City, city_id)
            if city:
                places_result.extend([place.to_dict() for place
                                      in city.places])
        if amenities_ids:
            amenities = [storage.get(Amenity, amenity_id)
                         for amenity_id in amenities_ids]
            amenities = [amenity for amenity in amenities
                         if amenity is not None]
            places_result = [
                place.to_dict() for place in places_result
                if all(amenity in place.amenities for amenity in amenities)
            ]
    return jsonify(places_result)
