from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime, timedelta
from flask_login import UserMixin
import os
import base64

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(10), index=True)
    last_name = db.Column(db.String(15), index=True)
    email = db.Column(db.String(70), index=True, unique=True)
    password = db.Column(db.String(128))
    country = db.Column(db.String(30))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration =db.Column(db.DateTime)
    favorites = db.relationship('Favorites', backref='user', lazy='dynamic')

    # Converts the password string into a hash
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), name="fk_user_id", nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id') , name="fk_restaurant_id", nullable=True)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(120), index=True)
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    street = db.Column(db.String(60))
    country = db.Column(db.String(60))
    rating = db.Column(db.Float)
    image = db.Column(db.String(120))
    foods = db.relationship('Food', backref='restaurant', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    favorites = db.relationship('Favorites', backref='restaurant', lazy='dynamic')

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(120), index=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(120))
    price = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    food_orders = db.relationship('FoodOrder', backref='food', lazy='dynamic')

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)
    order_total = db.Column(db.Float)
    delivery_address = db.Column(db.String(120))
    completed = db.Column(db.Boolean, default=False)
    cancelled = db.Column(db.Boolean, default=False)
    status = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_order = db.relationship('FoodOrder', backref='order', lazy='dynamic')

class FoodOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), name="fk_food_id", nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id') , name="fk_order_id", nullable=True)
    quantity = db.Column(db.Integer)
    side_note = db.Column(db.Text)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    image = db.Column(db.String(120))
    restaurants = db.relationship('Restaurant', backref='restaurant', lazy='dynamic')
