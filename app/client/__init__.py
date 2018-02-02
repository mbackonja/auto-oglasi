"""
Client application routes
"""

from flask import Blueprint, render_template, jsonify, request, session
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

    return render_template('index.html', user=session.get('user'))

@client.route('api/register', methods=['POST'])
def register():
    """
    Register new user
    """
    data = request.json
    database = mysql.get_db()
    cursor = database.cursor()

    cursor.execute("SELECT id FROM users WHERE email=%s", (data['email']))
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

    hashed_password = bcrypt.generate_password_hash(data['password'])
    cursor.execute(qurey, (data['name'], data['surname'], data['email'], hashed_password))

    database.commit()
    session['user'] = {'id': cursor.lastrowid, 'name': data['name'], 'surname': data['surname'],
                       'email': data['email']}
    return jsonify({'message': 'Successfully registered'}), 201

@client.route('api/login', methods=['POST'])
def login():
    """
    Login user
    """
    data = request.json
    database = mysql.get_db()
    cursor = database.cursor()

    if 'email' not in data or not data['email']:
        raise InvalidUsage("Email must not be empty", 422)
    if 'password' not in data or not data['password']:
        raise InvalidUsage("Password must not be empty", 422)

    cursor.execute("SELECT * FROM users WHERE email=%s", (data['email']))
    row = cursor.fetchone()
    if cursor.rowcount == 0:
        raise InvalidUsage("Wrong email or password", 401)

    if not bcrypt.check_password_hash(row['password'], data['password']):
        raise InvalidUsage("Wrong email or password", 401)

    user = {'id': row['id'], 'name': row['name'], 'surname': row['surname'], 'email': row['email']}
    session['user'] = user
    return jsonify(user)

@client.route('api/logout', methods=['POST'])
def logout():
    """
    Logout user
    """
    session.pop('user', None)
    return jsonify({'message': 'Successfully logged out'})

@client.route('api/cars')
def get_cars():
    """
    Get all cars
    """
    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT cars.id, car_makes.make, car_models.model, cars.year,
    cars.price, cars.km, cars.status
    FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id'''

    cursor.execute(query)
    cars = cursor.fetchall()

    return jsonify(cars)

@client.route('api/cars/<int:car_id>')
def get_car(car_id):
    """
    Get car
    """
    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT cars.id, car_makes.make, car_models.model, cars.year,
    cars.price, cars.km, cars.status, users.name, users.surname, cars.phone,
    cars.address, cars.kw, cars.hp, cars.ccm, cars.fuel_type,
    cars.description
    FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN users on cars.user_id = users.id
    WHERE cars.id = %s'''

    cursor.execute(query, (car_id))
    car = cursor.fetchone()

    return jsonify(car)

@client.route('api/my-cars')
def my_cars():
    """
    Get my cars
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT cars.id, car_makes.make, car_models.model, cars.year,
    cars.price, cars.km, cars.status, users.name, users.surname, cars.phone,
    cars.address, cars.kw, cars.hp, cars.ccm, cars.fuel_type,
    cars.description FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN users on cars.user_id = users.id
    WHERE users.id = %s'''

    cursor.execute(query, (session.get('user')['id']))
    cars = cursor.fetchall()

    return jsonify(cars)

@client.route('api/my-cars/<int:car_id>', methods=['DELETE'])
def delete_my_car(car_id):
    """
    Delete my car
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    database = mysql.get_db()
    cursor = database.cursor()

    query = '''DELETE FROM cars
    WHERE cars.id = %s AND user_id = %s'''

    numrows = cursor.execute(query, (car_id, session.get('user')['id']))
    database.commit()

    if numrows == 0:
        raise InvalidUsage('You don\'t have permission', 401)

    return jsonify({'message': 'Successfully deleted'}), 200

@client.route('api/users/personal', methods=['PUT'])
def update_user_personal_data():
    """
    Update user personal data
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    data = request.json
    if 'name' not in data or not data['name']:
        raise InvalidUsage("Name must not be empty", 422)
    if 'surname' not in data or not data['surname']:
        raise InvalidUsage("Surname must not be empty", 422)
    if 'currentPassword' not in data or len(data['currentPassword']) < 6:
        raise InvalidUsage("Current password must have more then 5 characters", 422)

    database = mysql.get_db()
    cursor = database.cursor()
    activeUser = session.get('user')

    query = '''SELECT password
    FROM users
    WHERE users.id = %s'''

    cursor.execute(query, (activeUser['id']))
    user = cursor.fetchone()

    if not bcrypt.check_password_hash(user['password'], data['currentPassword']):
        raise InvalidUsage("Wrong current password", 401)

    query = '''UPDATE users
    SET name = %s, surname = %s
    WHERE id = %s'''

    cursor.execute(query, (data['name'], data['surname'], session.get('user')['id']))
    database.commit()

    activeUser['name'] = data['name']
    activeUser['surname'] = data['surname']
    session['user'] = activeUser

    return jsonify({'message': 'Successfully updated'}), 200

@client.route('api/users/login', methods=['PUT'])
def update_user_login_data():
    """
    Update user login data
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    data = request.json
    if 'email' not in data or not data['email']:
        raise InvalidUsage("Email must not be empty", 422)
    if 'currentPassword' not in data or len(data['currentPassword']) < 6:
        raise InvalidUsage("Current password must have more then 5 characters", 422)
    if 'newPassword' not in data or len(data['newPassword']) < 6:
        raise InvalidUsage("New password must have more then 5 characters", 422)
    if 'newPasswordAgain' not in data or data['newPassword'] != data['newPasswordAgain']:
        raise InvalidUsage("New password does not match", 422)

    database = mysql.get_db()
    cursor = database.cursor()
    activeUser = session.get('user')

    query = '''SELECT password
    FROM users
    WHERE users.id = %s'''

    cursor.execute(query, (activeUser['id']))
    user = cursor.fetchone()

    if not bcrypt.check_password_hash(user['password'], data['currentPassword']):
        raise InvalidUsage("Wrong current password", 401)

    query = '''SELECT id
    FROM users
    WHERE users.email = %s AND users.id != %s'''

    cursor.execute(query, (data['email'], activeUser['id']))
    cursor.fetchone()

    if cursor.rowcount != 0:
        raise InvalidUsage("User with this email already exists", 422)

    query = '''UPDATE users
    SET email = %s, password = %s
    WHERE id = %s'''

    hashed_password = bcrypt.generate_password_hash(data['newPassword'])
    cursor.execute(query, (data['email'], hashed_password, session.get('user')['id']))
    database.commit()

    activeUser['email'] = data['email']
    session['user'] = activeUser

    return jsonify({'message': 'Successfully updated'}), 200
