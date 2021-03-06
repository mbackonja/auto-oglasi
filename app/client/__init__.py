"""
Client application routes
"""

from flask import Blueprint, render_template, jsonify, request, session
from flask_bcrypt import Bcrypt
from app.common.mysql import mysql
from app.common.invalid_usage_exception import InvalidUsage
from app.common.file_helper import is_allowed_file
from werkzeug.utils import secure_filename
from datetime import datetime
import shutil
import os

client = Blueprint('client', __name__, template_folder='templates', static_folder='static',  # pylint: disable=invalid-name
                   static_url_path='client/static')

bcrypt = Bcrypt()  # pylint: disable=invalid-name


allowed_condition = [ 'New', 'Used' ]
allowed_fuel_type = [ 'Diesel', 'Gasoline', 'LPG', 'Other' ]
allowed_sort_columns = [ 'id', 'price', 'year']
allowed_sort_directions = [ 'asc', 'desc' ]

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
                       'email': data['email'], 'is_admin': False}
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

    user = {'id': row['id'], 'name': row['name'], 'surname': row['surname'],
            'email': row['email'], 'is_admin': row['is_admin']}
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
    cars.price, cars.km, cars.status, cars_images.path as image_path
    FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN cars_images on cars.id = cars_images.car_id
    GROUP BY cars.id'''
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
    cars.address, cars.city, cars.kw, cars.hp, cars.ccm, cars.fuel_type,
    cars.description, car_models.id as model_id, car_makes.id as make_id
    FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN users on cars.user_id = users.id
    WHERE cars.id = %s'''
    cursor.execute(query, (car_id))
    car = cursor.fetchone()

    if not car:
        raise InvalidUsage('Car don\'t exists', 404)

    query = '''SELECT id, path
    FROM cars_images
    WHERE car_id = %s'''

    cursor.execute(query, (car_id))
    images = cursor.fetchall()

    car['images'] = images

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
    cars.description, cars_images.path as image_path
    FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN users on cars.user_id = users.id
    JOIN cars_images on cars.id = cars_images.car_id
    WHERE users.id = %s
    GROUP BY cars.id'''

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

    query = '''SELECT id
    FROM cars
    WHERE cars.id = %s AND user_id = %s'''
    numrows = cursor.execute(query, (car_id, session.get('user')['id']))
    if numrows == 0:
        raise InvalidUsage('You don\'t have permission', 401)


    image_path = os.path.join(os.path.abspath('app/static/img/cars'), str(car_id))
    shutil.rmtree(image_path)


    query = '''DELETE FROM cars_images
    WHERE cars_images.car_id = %s'''
    cursor.execute(query, (car_id))
    database.commit()

    query = '''DELETE FROM cars
    WHERE cars.id = %s'''
    cursor.execute(query, (car_id))
    database.commit()

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

@client.route('api/makes-and-models')
def get_cars_makes_and_models():
    """
    Get all car makes and models
    """
    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT *
    FROM car_models'''

    cursor.execute(query)
    car_models = cursor.fetchall()

    query = '''SELECT *
    FROM car_makes'''

    cursor.execute(query)
    car_makes = cursor.fetchall()
    response = { 'makes': car_makes, 'models': car_models }

    return jsonify(response)

@client.route('api/cars', methods=['POST'])
@client.route('api/cars/<int:car_id>', methods=['PUT'])
def create_new_car(car_id = None):
    """
    Create new car
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    isEditMode = True if car_id else False
    data = request.form
    database = mysql.get_db()
    cursor = database.cursor()

    if 'model' not in data or not data['model']:
        raise InvalidUsage("Car model must not be empty", 422)
    if 'year' not in data or not data['year']:
        raise InvalidUsage("Year must not be empty", 422)
    if 'price' not in data or not data['price']:
        raise InvalidUsage("Price must not be empty", 422)
    if 'mileage' not in data or not data['mileage']:
        raise InvalidUsage("Mileage must not be empty", 422)
    if 'condition' not in data or not data['condition']:
        raise InvalidUsage("Condition must not be empty", 422)
    if 'kw' not in data or not data['kw']:
        raise InvalidUsage("kW must not be empty", 422)
    if 'hp' not in data or not data['hp']:
        raise InvalidUsage("hp must not be empty", 422)
    if 'displacement' not in data or not data['displacement']:
        raise InvalidUsage("Displacement must not be empty", 422)
    if 'fuel_type' not in data or not data['fuel_type']:
        raise InvalidUsage("Fuel type must not be empty", 422)
    if 'description' not in data or not data['description']:
        raise InvalidUsage("Description must not be empty", 422)
    if 'phone' not in data or not data['phone']:
        raise InvalidUsage("Phone must not be empty", 422)
    if 'address' not in data or not data['address']:
        raise InvalidUsage("Address must not be empty", 422)
    if 'city' not in data or not data['city']:
        raise InvalidUsage("City must not be empty", 422)

    images = request.files.getlist('images')
    if not isEditMode: # if it's create mode
        if len(images) == 0:
            raise InvalidUsage("Must upload at least one image", 422)

    for image in images:
        if not is_allowed_file(image.filename):
            raise InvalidUsage("Image must be jpg/jpeg/bmp/png", 422)

    query = '''SELECT id
    FROM car_models
    WHERE id = %s'''
    cursor.execute(query, (data['model']))
    cursor.fetchone()
    if cursor.rowcount == 0:
        raise InvalidUsage("Uknown car model", 422)

    
    if not data['year'].isdigit() or int(data['year']) < 0 or int(data['year']) > datetime.now().year:
        raise InvalidUsage("Invalid year", 422)
    if not data['price'].isdigit() or int(data['price']) <= 0:
        raise InvalidUsage("Price must be positive number", 422)
    if not data['mileage'].isdigit() or int(data['mileage']) <= 0:
        raise InvalidUsage("Mileage must be positive number", 422)
    if not data['kw'].isdigit() or int(data['kw']) <= 0:
        raise InvalidUsage("kW must be positive number", 422)
    if not data['hp'].isdigit() or int(data['hp']) <= 0:
        raise InvalidUsage("hp must be positive number", 422)
    if not data['condition'] or not data['condition'] in allowed_condition:
        raise InvalidUsage("Condition invalid", 422)
    if not data['fuel_type'] or not data['fuel_type'] in allowed_fuel_type:
        raise InvalidUsage("Fuel type invalid", 422)

    if not isEditMode: # If it's create mode
        query = '''INSERT INTO
        cars(model_id, user_id, year, price, km, status, kw, hp, ccm, fuel_type, description, phone, address, city)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        cursor.execute(query,
                    (data['model'], session.get('user')['id'], data['year'],
                    data['price'], data['mileage'], data['condition'], data['kw'],
                    data['hp'], data['displacement'], data['fuel_type'], data['description'],
                    data['phone'], data['address'], data['city']))
        database.commit()
        car_id = cursor.lastrowid
    else:
        query = '''UPDATE cars
        SET model_id = %s, user_id = %s, year = %s, price = %s, km = %s, status = %s, kw = %s, hp = %s, ccm = %s, fuel_type = %s, description = %s, phone = %s, address = %s, city = %s
        WHERE cars.id = %s'''

        cursor.execute(query,
                    (data['model'], session.get('user')['id'], data['year'],
                    data['price'], data['mileage'], data['condition'], data['kw'],
                    data['hp'], data['displacement'], data['fuel_type'], data['description'],
                    data['phone'], data['address'], data['city'], car_id))
        database.commit()

    image_path = os.path.join(os.path.abspath('app/static/img/cars'), str(car_id))
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    query = '''INSERT INTO
    cars_images(car_id, path)
    VALUES(%s, %s)'''

    images = request.files.getlist('images')

    for image in images:
        filename = secure_filename(image.filename)
        image.save(os.path.join(image_path, filename))
        cursor.execute(query, (car_id, filename))
        database.commit()

    if isEditMode:
        return jsonify({'message': 'Successfully edited'}), 200
    else:
        return jsonify({'message': 'Successfully added'}), 201
        

@client.route('api/cars/<int:car_id>/images/<int:image_id>', methods=['DELETE'])
def delete_car_image(car_id, image_id):
    """
    Delete car image
    """
    if not 'user' in session:
        raise InvalidUsage("Access denied", 401)

    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT path
    FROM cars_images
    JOIN cars on cars_images.car_id = cars.id
    WHERE cars.user_id = %s AND cars_images.id = %s and cars.id = %s'''

    cursor.execute(query, (session.get('user')['id'], image_id, car_id))
    image = cursor.fetchone()

    if not image:
        raise InvalidUsage('Image don\'t exists', 404)

    image_path = os.path.join(os.path.abspath('app/static/img/cars'), str(car_id), image['path'])
    os.remove(image_path)

    query = '''DELETE FROM cars_images
    WHERE cars_images.id = %s'''

    cursor.execute(query, (image_id))
    database.commit()

    return jsonify({'message': 'Successfully deleted'}), 200

@client.route('api/cars/search', methods=['POST'])
def car_search():
    """
    Search cars
    """
    data = request.json
    database = mysql.get_db()
    cursor = database.cursor()

    query = '''SELECT cars.id, car_makes.make, car_models.model, cars.year,
    cars.price, cars.km, cars.status, cars_images.path as image_path
    FROM cars
    JOIN car_models on cars.model_id = car_models.id
    JOIN car_makes on car_models.make_id = car_makes.id
    JOIN cars_images on cars.id = cars_images.car_id'''

    queryData = []

    if 'make' in data and len(data['make']) > 0:
        query += ' WHERE car_makes.id = %s'
        queryData.append(data['make'])

    if 'model' in data and len(data['model']) > 0:
        if len(queryData) > 0:
            query += ' AND'
        else:
            query += ' WHERE'
        query += ' car_models.id = %s'
        queryData.append(data['model'])

    if 'priceFrom' in data and str(data['priceFrom']).isdigit():
        if len(queryData) > 0:
            query += ' AND'
        else:
            query += ' WHERE'
        query += ' cars.price >= %s'
        queryData.append(data['priceFrom'])

    if 'priceTo' in data and str(data['priceTo']).isdigit():
        if len(queryData) > 0:
            query += ' AND'
        else:
            query += ' WHERE'
        query += ' cars.price <= %s'
        queryData.append(data['priceTo'])

    if 'fuelType' in data and data['fuelType'] in allowed_fuel_type:
        if len(queryData) > 0:
            query += ' AND'
        else:
            query += ' WHERE'
        query += ' cars.fuel_type = %s'
        queryData.append(data['fuelType'])

    query += ' GROUP BY cars.id'

    if 'sortBy' in data:
        sortData = data['sortBy'].split('-')
        if sortData[0] in allowed_sort_columns and sortData[1] in allowed_sort_directions:
            query += ' ORDER BY ' + sortData[0] + ' ' + sortData[1]

    cursor.execute(query, tuple(queryData))
    cars = cursor.fetchall()

    return jsonify(cars)