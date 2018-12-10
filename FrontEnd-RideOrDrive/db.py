from flaskapp import app
from flask_pymongo import PyMongo

mongo = PyMongo(app)
appDB = mongo.db