from app import app, db
from flask import Flask, abort, request
from app.models import User
import json
from flask import jsonify
from flask_cors import CORS
from app.api.auth import basic_auth
from werkzeug.security import generate_password_hash, check_password_hash
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
    psswd = generate_password_hash(user['password'])
    u = User(first_name=str(user['first-name']), last_name=str(user['last-name']),
        email=str(user['email']), password=psswd)
    db.session.add(u)
    db.session.commit()
    return json.dumps(user)

@app.post("/login")
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})


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