import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "IAMSAFSU"

db_username = os.environ['MYSQL_USER']
db_password = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_hostname = os.environ['MYSQL_HOSTNAME']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(db_username, db_password, db_hostname, db_name)

db = SQLAlchemy(app)

from app import routes