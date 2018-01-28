"""
Main app module
"""

from flask import Flask, render_template, jsonify
from app.client import client
from app.admin import admin
from app.common.mysql import mysql
from app.common.invalid_usage_exception import InvalidUsage

app = Flask(__name__) # pylint: disable=invalid-name
app.config.from_envvar('AUTOOGLASI_SETTINGS')

app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    Invalid Usage Exception Handler
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


mysql.init_app(app)

@app.route('/<path:path>')
def catch_all(path): # pylint: disable=unused-argument
    """
    Catch all route
    """
    return render_template('index.html')
