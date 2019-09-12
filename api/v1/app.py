#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')
db = os.environ.get('HBNB_TYPE_STORAGE', 'jsonfile')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(cls):
    """ close session """
    storage.close()


@app.errorhandler(404)
def error(e):
    """ error 404 handler """
    return (jsonify({"error": "Not found"}),  404)


if __name__ == '__main__':
    """ starts api """
    app.run(host=host, port=port, threaded=True)
