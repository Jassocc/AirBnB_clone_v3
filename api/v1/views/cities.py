#!/usr/bin/python3

"""
Cities Route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_in_state(state_id=None):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities_in_state = [city.to_json() for city in state.cities]
    return jsonify(cities_in_state)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_get(city_id=None):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id=None):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_add(state_id=None):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(city_id=None):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return 'Not a JSON', 400
    if data is None:
        return 'Not a JSON', 400
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at', 'state_id'):
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_json())
