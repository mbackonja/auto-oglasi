"""
Main app module
"""

from flask import Flask
from app.client import client
from app.admin import admin

app = Flask(__name__) # pylint: disable=invalid-name
app.config.from_pyfile('config.py')

app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
