from flask import jsonify
from app import db
from app.api import bp
from app import app
from app.api.auth import basic_auth

@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})