from app import app, db
from flask import Flask, abort, request
from app.models import User
import json
from flask import jsonify
from flask_cors import CORS
from app.api.auth import basic_auth
from werkzeug.security import generate_password_hash, check_password_hash
CORS(app)
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

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
    psswd = generate_password_hash(user['password'])
    u = User(first_name=str(user['first-name']), last_name=str(user['last-name']),
        email=str(user['email']), password=psswd)
    db.session.add(u)
    db.session.commit()
    return json.dumps(user)

# Logs in the user
@app.post("/login")
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

@app.get("/user-profile/<string:t>")
def get_user(t):
    u = db.session.query(User).filter_by(token=t).first()
    
    out = {
        "id": u.id,
        "name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "phone": u.phone,
        "password": u.password,
        "country": u.country,
        "token": u.token
    }
    return json.dumps(out)

@app.post("/user-profile")
def edit_user():
    user = request.get_json()
    u = User.query.get(str(user['id']))
    
    u.first_name = str(user['name'])
    u.last_name = str(user['last_name'])
    u.email = str(user['email'])
    u.password = str(user['password'])
    u.phone = str(user['phone'])
    u.country = str(user['country'])
    db.session.commit()
    return json.dumps(user)

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