from models.user_model import UserModel
from werkzeug.security import safe_str_cmp

# Function to perform authentication.
def authenticate( username, password):
    user_to_find = UserModel.get_user_by_name( username)
    if user_to_find is not None and safe_str_cmp(user_to_find.password, password):
        return user_to_find

# Function to check if user is already authenticated.
def is_authenticated( payload):
    user_id = payload["identity"]
    return UserModel.get_user_by_id( user_id)
