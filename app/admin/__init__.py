"""
Admin application routes
"""

from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates') # pylint: disable=invalid-name

@admin.route('/')
def hello_world():
    """
    Hello world
    """

    return 'Hello, Admin!'
