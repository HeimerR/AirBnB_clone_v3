from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/<id>')
@app_views.route('/states')
def state(id=None):
    states = []
    if id:
        state = storage.get("State", id)
        if state is None:
            abort(404, description="Resource not found")
        else:
            return jsonify(state.to_dict())

    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<id>', methods=['DELETE'])
def state_delete(id=None):
    state = storage.get("State", id)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/states', methods=['POST'])
def state_post():
    new = request.get_json()
    new_obj = State(**new)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
