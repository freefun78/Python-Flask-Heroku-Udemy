# This file is to overcome app.py runs locally incompatibility with running using uwsgi on heroku
from app import app
from db import db

# Init the db here
db.init_app(app)

# Add decorator here, delete the one from app.py
@app.before_first_request
def create_tables():
    db.create_all()