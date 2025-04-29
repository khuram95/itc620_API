# api/login.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
import datetime
from db import db, Users
import sys # for debugging
login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['POST'])
def login():
    print(request.headers, file=sys.stderr)
    print(request.data, file=sys.stderr)
    print(request.json, file=sys.stderr) 
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create a JWT token with an expiration time of 30 minutes
    token_payload = {
        'user_id': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'is_admin': user.is_admin
    }
    token = jwt.encode(
        token_payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'user_id': user.user_id,
            'email': user.email
        }
    })
