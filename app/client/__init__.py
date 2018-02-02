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

@client.route('api/products')
def get_products():
    """
    Get all products
    """
    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT products.id, car_makes.make, car_models.model, products.year,
    products.price, products.km, products.status FROM products
    JOIN car_models on products.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id'''

    cursor.execute(query)
    products = cursor.fetchall()

    return jsonify(products)

@client.route('api/products/<int:product_id>')
def get_product(product_id):
    """
    Get product
    """
    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT products.id, car_makes.make, car_models.model, products.year,
    products.price, products.km, products.status, users.name, users.surname, products.phone,
    products.address, products.kw, products.hp, products.ccm, products.fuel_type,
    products.description FROM products
    JOIN car_models on products.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN users on products.user_id = users.id
    WHERE products.id = %s'''

    cursor.execute(query, (product_id))
    product = cursor.fetchone()

    return jsonify(product)

@client.route('api/my-products')
def my_products():
    """
    Get my products
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT products.id, car_makes.make, car_models.model, products.year,
    products.price, products.km, products.status, users.name, users.surname, products.phone,
    products.address, products.kw, products.hp, products.ccm, products.fuel_type,
    products.description FROM products
    JOIN car_models on products.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN users on products.user_id = users.id
    WHERE users.id = %s'''

    cursor.execute(query, (session.get('user')['id']))
    products = cursor.fetchall()

    return jsonify(products)

@client.route('api/my-products/<int:product_id>', methods=['DELETE'])
def delete_my_product(product_id):
    """
    Delete my product
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    database = mysql.get_db()
    cursor = database.cursor()

    query = '''DELETE FROM products
    WHERE products.id = %s AND user_id = %s'''

    numrows = cursor.execute(query, (product_id, session.get('user')['id']))
    database.commit()

    if numrows == 0:
        raise InvalidUsage('You don\'t have permission', 401)

    return jsonify({'message': 'Successfully deleted'}), 200
