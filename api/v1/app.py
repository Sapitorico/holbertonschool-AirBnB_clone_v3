#!/usr/bin/python3
"""application"""
from flask import Flask, make_response, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

"""instancies my app"""
app = Flask(__name__)
"""register blueprint template in my appi"""
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "*"}})



@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    """run my app"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 500))
    app.run(host=host, port=port, threaded=True)
