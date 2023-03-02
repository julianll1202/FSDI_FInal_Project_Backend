from app import app, db
from flask import Flask, abort, request
from app.models import User, Restaurant, Food, Orders, FoodOrder, Category, Favorites
import json
from flask import jsonify
from flask_cors import CORS
from app.api.auth import basic_auth, token_auth
from app.api import bp
from werkzeug.security import generate_password_hash, check_password_hash
CORS(app)
from sqlalchemy import select, desc
from sqlalchemy.orm import sessionmaker
from datetime import time, datetime
from flask_login import current_user, login_user, login_required, logout_user

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
    u = basic_auth.current_user()
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

@app.get("/user/logout")
def logout_user():
    logout_user()
    return ("User is logged out")

@app.post("/user-profile/<string:t>")
@token_auth.login_required
def get_user(t):
    # u = db.session.query(User).filter_by(token=t).first()
    u = basic_auth.current_user()
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
@token_auth.login_required
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
            "rating": r.rating,
            "image": str(r.image)
        }
        rest_list.append(res)
    return rest_list

@app.get("/restaurant/<int:id>")
def get_restaurant(id):
    r = Restaurant.query.get(id)
    out = {
        "id": r.id,
        "name": r.restaurant_name,
        "rating": r.rating,
        "image": str(r.image),
        "opening_time": r.opening_time.strftime("%H:%M"),
        "closing_time": r.closing_time.strftime("%H:%M"),
        "street": r.street,
        "country": r.country
    }
    return json.dumps(out)

def get_restaurant_name(id):
    r = Restaurant.query.get(id)
    out = {
        "rest_name": r.restaurant_name
    }
    return r.restaurant_name

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

@app.put("/restaurant")
def edit_restaurant():
    rest = request.get_json()
    r = Restaurant.query.get(str(rest['id']))
    r.name = str(rest['name'])
    open = time(int(str(rest['opening_time'])[:2]), int(str(rest['opening_time'])[3:5]),int(str(rest['opening_time'])[6:]))
    close = time(int(str(rest['closing_time'])[:2]), int(str(rest['closing_time'])[3:5]),int(str(rest['closing_time'])[6:]))
    r.opening_time = open
    r.closing_time = close
    r.street = str(rest['street'])
    r.country = str(rest['country'])
    r.rating = str(rest['rating'])
    r.image = str(rest['image'])
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
            "desc": food.description,
            "restaurant_id": food.restaurant_id
        }
        menu_list.append(f)
    return menu_list

@app.get("/food/details/<int:id>")
def get_food_details(id):
    f = Food.query.get(id)
    rest_name = get_restaurant_name(f.restaurant_id)
    food = {
        "id": f.id,
        "name": f.food_name,
        "description": f.description,
        "image": f.image,
        "price": f.price,
        "restaurant_id": f.restaurant_id,
        "restaurant_name": rest_name
    }

    return json.dumps(food)

@app.put("/food")
def edit_food():
    data = request.get_json()
    food = Food.query.get(int(data['id']))
    food.name = str(data['name'])
    food.description = str(data['desc'])
    food.price = float(data['price'])
    food.image = str(data['image'])
    food.restaurant_id = int(data['rest_id'])
    db.session.commit()
    return json.dumps(data)

@app.delete("/food/<int:id>")
def delete_food(id):
    food = Food.query.get(id)
    db.session.delete(food)
    db.session.commit()
    return "Food was deleted"

######################################
#       FAVORITES ENDPOINTS          #
######################################
@app.get("/user/<int:id>/favorite")
def get_favorites(id):
    favorites = []
    favs = db.session.query(Favorites).filter_by(user_id=id).all()
    for fav in favs:
        res_info = Restaurant.query.get(int(fav.restaurant_id))
        f = {
            "fav_id":fav.id,
            "name": res_info.restaurant_name,
            "rest_id": res_info.id,
            "name": res_info.restaurant_name,
            "rating": res_info.rating,
            "image": str(res_info.image)
        }
        favorites.append(f)
    return favorites

@app.post("/favorite")
def add_favorite():
    new_fav = request.get_json()
    favs = get_favorites(int(new_fav['user_id']))
    for f in favs:
        if int(new_fav['rest_id']) == f['rest_id']:
            return json.dumps(new_fav)
    fav = Favorites(user_id=int(new_fav['user_id']), restaurant_id=int(new_fav['rest_id']))
    db.session.add(fav)
    db.session.commit()
    return json.dumps(new_fav)

@app.delete("/favorite")
def remove_favorite():
    new_fav = request.get_json()
    fav = Favorites.query.get(int(new_fav['fav_id']))
    db.session.delete(fav)
    db.session.commit()
    return json.dumps(new_fav)

######################################
#       CATEGORY ENDPOINTS           #
######################################
@app.get("/category")
def get_categories():
    cat = Category.query.all()
    categories = []
    for c in cat:
        category = {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "image": c.image
        }
        categories.append(category)
    return categories

@app.post("/category")
def create_category():
    data = request.get_json()
    cat = Category(name=str(data['name']), description=str(data['description']), image=str(data['image']))
    db.session.add(cat)
    db.session.commit()
    return data

@app.put("/category")
def edit_category():
    data = request.get_json()
    cat = Category.query.get(int(data['id']))
    cat.name = str(data['name'])
    cat.description=str(data['description'])
    cat.image=str(data['image'])
    db.session.commit()
    return json.dumps(data)

######################################
#          ORDER ENDPOINTS           #
######################################
@app.get("/orders")
def get_orders_list():
    o = Orders.query.all()
    orders = []
    for order in o:
        ordr = {
            "id": order.id,
            "order_date": order.order_date,
            "order_total": order.order_total,
            "delivery_address": order.delivery_address,
            "user_id": order.user_id
        }
        orders.append(ordr)
    return orders

@app.get("/user/order/<int:id>")
def get_order(id):
    o = Orders.query.get(id)
    # foods = db.session.query(FoodOrder).filter_by(order_id=id).all()
    foods = db.session.query(Food).join(FoodOrder).filter(FoodOrder.order_id==id).all()
    food_list = []
    for food in foods:
        f = {
            "id": food.id,
            "name": food.food_name,
            "price": food.price,
            "restaurant_id": food.restaurant_id
        }
        food_list.append(f)
   
    res = Restaurant.query.get(int(food_list[0]['restaurant_id']))
    order = {
        "id": o.id,
        "order_total": o.order_total,
        "delivery_address": o.delivery_address,
        "order_date": str(o.order_date),
        "status": o.status,
        "products": food_list,
        "restaurant_name": res.restaurant_name,
        "rest_img": res.image
    }
    return order

@app.post("/order")
def create_order():
    data = request.get_json()
    today = datetime.now()
    new_order = Orders(order_date=today, order_total=float(data['order_total']),
        delivery_address=str(data['delivery_address']), 
        status="Restaurant is receiving your order", user_id=int(data['user_id'])
    )
    db.session.add(new_order)
    current_order = db.session.query(Orders).filter_by(user_id=int(data['user_id'])).order_by(desc(Orders.id)).first()
    #cur_order_query = select(Orders.id).where(Orders.user_id==int(data['user_id'])).order_by(desc(Orders.id)).limit(1)
    # current_order = db.session.execute(cur_order_query)
    for food in data['items']:
        new_food_order = FoodOrder(food_id=food['food_id'],order_id=current_order.id, 
            quantity=food['quantity'], side_note=food['side_notes'])
        db.session.add(new_food_order)
    db.session.commit()
    return json.dumps(data)

@app.get("/user/<int:id>/orders")
def get_past_orders(id):
    orders = db.session.query(Orders).filter(Orders.user_id==id).all()
    past_orders = []
    for order in orders:
        o = get_order(order.id)
        past_orders.append(o)
    return past_orders

# def get_user_food_orders(order_id):
#     food_orders = db.session.query(FoodOrder).filter(FoodOrder.order_id==order_id).all()
#     foods = []
#     for food in food_orders:
#         f = get_food_details(f.food_id)
#         food.append(f)
#     return foods

@app.get("/food-orders")
def get_food_order_list():
    food_orders = FoodOrder.query.all()
    data = []
    for food_order in food_orders:
        entry = {
            "food_id": food_order.food_id,
            "order_id": food_order.order_id,
            "quantity": food_order.quantity,
            "side_note": food_order.side_note
        }
        data.append(entry)
    return data

@app.get("/food-order/<int:id>")
def get_food_order(id):
    food_order = FoodOrder.query.get(id)
    out = {
        "id": food_order.id,
        "food_id": food_order.food_id,
        "order_id": food_order.order_id,
        "quantity": food_order.quantity,
        "side_note": food_order.side_note
    }
    return json.dumps(out)

@app.delete("/order/<int:id>")
def delete_order(id):
    order = Orders.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return json.dumps("Order deleted")