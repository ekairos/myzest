from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from myzest import config

"""
App config
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
bcrypt = Bcrypt(app)

"""
MongoDB Config
"""
app.config['MONGO_URI'] = config.mongo_uri

mongo = PyMongo(app)

from myzest import routes
