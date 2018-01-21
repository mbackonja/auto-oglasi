"""
Admin application routes
"""

from flask import Blueprint, render_template

client = Blueprint('client', __name__, template_folder='templates') # pylint: disable=invalid-name

@client.route('/')
def hello_world():
    """
    Hello world
    """

    return render_template('index.html')
