#!/usr/bin/python3
"""
app file for api
"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """
    teardown calling close
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    handles 404 errors and return a response
    """
    return (jsonify({"error": "Not Found"}), 404)

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
