from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(10), index=True)
    last_name = db.Column(db.String(15), index=True)
    email = db.Column(db.String(70), index=True, unique=True)
    password = db.Column(db.String(20))

    # Converts the password string into a hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
