"""
Main app module
"""

from flask import Flask, render_template
from app.client import client
from app.admin import admin
from app.db import mysql

app = Flask(__name__) # pylint: disable=invalid-name
app.config.from_envvar('AUTOOGLASI_SETTINGS')

app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')

mysql.init_app(app)

@app.route('/<path:path>')
def catch_all(path): # pylint: disable=unused-argument
    """
    Catch all route
    """
    return render_template('index.html')
