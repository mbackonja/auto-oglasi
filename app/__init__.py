"""
Main app module
"""

from flask import Flask
from app.routes import routes

app = Flask(__name__) # pylint: disable=invalid-name
app.config.from_object('app.config')
app.register_blueprint(routes)
