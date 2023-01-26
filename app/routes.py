from app import app, db
from flask import Flask, abort, request
from app.models import User
import json
from flask_cors import CORS

CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
@app.route('/julian')
def my_name():
    return "Hi, my name is Julian"

@app.post("/signup")
def save_user():
    user = request.get_json()

    if user is None:
        return abort(400, "User could not be created")
    u = User(first_name=str(user['first-name']), last_name=str(user['last-name']),
        email=str(user['email']), password=str(user['password']))
    db.session.add(u)
    db.session.commit()
    return json.dumps(user)