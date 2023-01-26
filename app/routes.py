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

# Creates a new user through the sign up form
@app.post("/signup")
def save_user():
    user = request.get_json()
    users = get_all_users()
    for usr in users:
        if user['email'] == usr['email']:
            return abort(208, "Email already on database")
    if user is None:
        return abort(400, "User could not be created")
    u = User(first_name=str(user['first-name']), last_name=str(user['last-name']),
        email=str(user['email']), password=str(user['password']))
    db.session.add(u)
    db.session.commit()
    return json.dumps(user)

@app.post("/login")
def validate_user_cred():
    user_cred = request.get_json()
    users = get_all_users()
    for usr in users:
        if user_cred['email'] == usr['email']:
            if user_cred['password'] == usr['password']:
                return json.dumps(usr)
            else:
                return abort(400, "Invalid user credentials")

# Gets the list of all the users
@app.get("/user-list")
def get_all_users():
    users = User.query.all()
    user_list = []
    for u in users:
        usr ={
            "id": u.id,
            "first-name": u.first_name,
            "last-name": u.last_name,
            "email": u.email,
            "password": u.password
        }
        user_list.append(usr)
    return user_list