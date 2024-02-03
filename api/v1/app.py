#!/usr/bin/python3
"""
app file for api
"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown calling close
    """
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
