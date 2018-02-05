"""
Admin application routes
"""

from flask import Blueprint, jsonify, request, session
from app.common.invalid_usage_exception import InvalidUsage
from app.common.mysql import mysql
import shutil
import os


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static') # pylint: disable=invalid-name

@admin.route('/api/cars')
def my_cars():
    """
    Get cars
    """
    if not 'user' in session or not session['user']['is_admin']:
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
    GROUP BY cars.id'''

    cursor.execute(query)
    cars = cursor.fetchall()

    return jsonify(cars)

@admin.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """
    Delete car
    """
    if not 'user' in session or not session['user']['is_admin']:
        raise InvalidUsage("Access denied", 401)

    database = mysql.get_db()
    cursor = database.cursor()

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
