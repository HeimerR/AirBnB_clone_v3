#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(cls):
    storage.close()


@app.errorhandler(404)
def error(e):
    return (jsonify({"error": "Not found"}),  404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
