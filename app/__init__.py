from flask import Flask
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "IAMSAFSU"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'urvish'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'tweeter'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://urvish:root@localhost/tweeter'

db = SQLAlchemy(app)
mysql = MySQL(app)

from app import routes