from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import os
from os import path
from myzest import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config.secret_key
app.config['RECIPE_PIC_DIR'] = path.join(path.dirname(path.realpath(__file__)),
                                         'static/img/recipes/')
app.config['USER_PIC_DIR'] = path.join(path.dirname(path.realpath(__file__)),
                                       'static/img/users/')

bcrypt = Bcrypt(app)

"""
Set MongoDB URI for Testing and Dev ENV
for testing ENV run 'TEST_FLAG=true python -m unittest'
"""

app.config['MONGO_URI'] = config.test_mongo_uri if os.environ.get('TEST') \
    else config.mongo_uri

mongo = PyMongo(app)

from myzest import main
