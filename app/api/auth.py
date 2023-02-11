from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from flask import request

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(user, passw):
    cred = request.get_json()
    user = User.query.filter_by(email=str(cred['email'])).first()
    if user and user.check_password(str(cred['password'])):
        return user

@token_auth.verify_token
def verify_token(t):
    tok = request.get_json()
    token = str(tok['token'])
    return User.check_token(token) if token else None

