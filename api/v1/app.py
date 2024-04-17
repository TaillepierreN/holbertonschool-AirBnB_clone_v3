#!/usr/bin/python3
"""web app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """close db"""
    storage.close()


if __name__ == "__main__":
    API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    API_PORT = getenv("HBNB_API_PORT", 5000)
    app.run(host=API_HOST, port=API_PORT, threaded=True)