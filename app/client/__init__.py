"""
Client application routes
"""

from flask import Blueprint, render_template, jsonify, request
from flask_bcrypt import Bcrypt
from app.common.mysql import mysql
from app.common.invalid_usage_exception import InvalidUsage

client = Blueprint('client', __name__, template_folder='templates', static_folder='static',  # pylint: disable=invalid-name
                   static_url_path='client/static')

bcrypt = Bcrypt()  # pylint: disable=invalid-name
@client.route('/')
def index():
    """
    Return angular application
    """

    return render_template('index.html')

@client.route('api/register', methods=['POST'])
def register():
    """
    Register new user
    """
    data = request.json
    database = mysql.get_db()
    cursor = database.cursor()

    cursor.execute('SELECT id FROM users WHERE email=%s', (data['email']))
    cursor.fetchone()
    if cursor.rowcount != 0:
        raise InvalidUsage("User with same email already registered", 409)

    if 'name' not in data or not data['name']:
        raise InvalidUsage("Name must not be empty", 422)
    if 'surname' not in data or not data['surname']:
        raise InvalidUsage("Surname must not be empty", 422)
    if 'email' not in data or not data['email']:
        raise InvalidUsage("Email must not be empty", 422)
    if 'password' not in data or len(data['password']) < 6:
        raise InvalidUsage("Password must have more then 5 characters", 422)
    if 'passwordAgain' not in data or data['password'] != data['passwordAgain']:
        raise InvalidUsage("Password does not match", 422)

    qurey = '''INSERT INTO
    users(name, surname, email, password)
    VALUES(%s, %s, %s, %s)'''

    hashed_password = bcrypt.generate_password_hash(data["password"])
    cursor.execute(qurey, (data["name"], data["surname"], data["email"], hashed_password))

    database.commit()
    return jsonify({"message": "Successfully registered"}), 201
