from flask import Flask
from flask_pymongo import PyMongo
from myzest import config

"""
App config
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key

"""
MongoDB Config
"""
app.config['MONGO_URI'] = config.mongo_uri

mongo = PyMongo(app)

from myzest import routes
