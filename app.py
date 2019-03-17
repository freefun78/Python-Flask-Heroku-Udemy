import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS, cross_origin
from security import authenticate, is_authenticated
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# Access heroku DATABASE_URL environment variable with sqlite as alternative when not found (i.e. run locally)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "testApi11"

api = Api(app)

CORS(app)


# Instantiate JWT passing function defined for authentication and authentication state as parameters.
jwt = JWT( app, authenticate, is_authenticated)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, "/register")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# Ensure only run only in main module, avoid accidental run twice during multiple nested import.
if __name__ == "__main__" :
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)

