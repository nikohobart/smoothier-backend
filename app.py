from flask import Flask
from flask_restful import Api
import os

from db import db
from resources.recipe import Recipe


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Recipe, '/recipe/')

db.init_app(app)

if __name__ == '__main__':
  app.run(port=5000, debug=False)