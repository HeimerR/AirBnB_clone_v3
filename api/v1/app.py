#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')
app = Flask(__name__)
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
    app.run(host=host, port=port, threaded=True)
