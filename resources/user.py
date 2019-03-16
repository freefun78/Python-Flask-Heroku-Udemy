import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource) :
    parser = reqparse.RequestParser();
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Name parameter is required.")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Password parameter is required.")
    def post(self):
        data = UserRegister.parser.parse_args()
        user_found = UserModel.get_user_by_name( data['username'])

        if user_found :
            return {"message": "User already exists"}, 400

        new_user = UserModel( **data)
        new_user.save_to_db()

        return {"message": "User is successfully registered"}, 201



