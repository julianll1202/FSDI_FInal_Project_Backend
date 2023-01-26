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