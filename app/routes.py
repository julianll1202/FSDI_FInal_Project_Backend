from app import app, db
from flask import Flask, abort, request
from app.models import User, Restaurant, Food, Orders, FoodOrder
import json
from flask import jsonify
from flask_cors import CORS
from app.api.auth import basic_auth
from werkzeug.security import generate_password_hash, check_password_hash
CORS(app)
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from datetime import time

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
@app.route('/julian')
def my_name():
    return "Hi, my name is Julian"

######################################
#           USER ENDPOINTS           #
######################################
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

######################################
#     RESTAURANT ENDPOINTS           #
######################################

@app.get("/home")
def get_restaurant_list():
    rest = Restaurant.query.all()
    rest_list = []
    for r in rest:
        res = {
            "id": r.id,
            "name": r.restaurant_name,
            "rating": r.rating
        }
        rest_list.append(res)
    return rest_list

@app.post("/restaurant")
def create_restaurant():
    rest = request.get_json()
    open = time(int(str(rest['opening_time'])[:2]), int(str(rest['opening_time'])[3:5]),int(str(rest['opening_time'])[6:]))
    close = time(int(str(rest['closing_time'])[:2]), int(str(rest['closing_time'])[3:5]),int(str(rest['closing_time'])[6:]))
    r = Restaurant(restaurant_name=str(rest['name']), opening_time = open,
        closing_time = close, street = str(rest['street']),
        country = str(rest['country']), rating = str(rest['rating']))
    db.session.add(r)
    db.session.commit()
    return json.dumps(rest)

@app.post("/food")
def create_food():
    food = request.get_json()
    f = Food(food_name=str(food['name']), description=str(food['desc']),
        image=str(food['image']),price=float(str(food['price'])), 
        restaurant_id=int(str(food['rest_id'])))
    db.session.add(f)
    db.session.commit()
    return json.dumps(food)

@app.get("/menu/<int:id>")
def get_restaurant_menu(id):
    menu = db.session.query(Food).filter_by(restaurant_id=id).all()
    menu_list = []
    for food in menu:
        f = {
            "id": food.id,
            "name": food.food_name,
            "image": food.image,
            "price": food.price,
            "restaurant_id": food.restaurant_id
        }
        menu_list.append(f)
    return menu_list

@app.get("/food/details/<int:id>")
def get_food_details(id):
    f = Food.query.get(id)
    food = {
            "id": f.id,
            "name": f.food_name,
            "description": f.description,
            "image": f.image,
            "price": f.price,
            "restaurant_id": f.restaurant_id
    }

    return json.dumps(food)