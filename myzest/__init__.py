"""MyZest is an online cookbook running Python3.6, Flask framework and
MongoDB Atlas.

The 'main' module contains the whole application logic and Flask routing.
Here the Flask app is initialized and configured along with the MongoDB
connection using a 'config' module to hold sensitive data.

IMPORTANT !!!
To avoid circular import problems, import the main module at the very bottom
as it uses the setup below.
See: Corey Schafer https://youtu.be/44PvX0Yv368

.. warning:: Minimum Viable Product not met yet !
"""

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
