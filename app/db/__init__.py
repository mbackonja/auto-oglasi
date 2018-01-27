"""
MySQL instance shared between all blueprints
"""

from flaskext.mysql import MySQL
import pymysql

mysql = MySQL(cursorclass=pymysql.cursors.DictCursor)  # pylint: disable=invalid-name
