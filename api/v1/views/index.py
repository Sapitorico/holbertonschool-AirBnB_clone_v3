#!/usr/bin/python3
"""index of my application"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def index():
    """returned a object with json representation"""
    return jsonify({"status": "OK"})
