#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

"""instancies my app"""
app = Flask(__name__)

"""register blueprint template in my appi"""
app.register_blueprint(app_views)


host = getenv('HBNB_API_HOST', '0.0.0.0')
port = int(getenv('HBNB_API_PORT', 500))


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()


if __name__ == '__main__':
    """run my app"""
    app.run(host=host, port=port, threaded=True)
