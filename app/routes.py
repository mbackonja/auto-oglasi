"""
Application routes
"""

from flask import Blueprint

routes = Blueprint('routes', __name__) # pylint: disable=invalid-name

@routes.route('/')
def hello_world():
    """
    Hello world
    """

    return 'Hello, World!'
