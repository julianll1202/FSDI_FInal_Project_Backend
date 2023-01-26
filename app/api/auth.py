from flask_httpauth import HTTPBasicAuth
from app.models import User
from flask import request
basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(user, passw):
    cred = request.get_json()
    user = User.query.filter_by(email=str(cred['email'])).first()
    if user and user.check_password(str(cred['password'])):
        return user