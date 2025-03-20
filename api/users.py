# api/users.py
from flask import Blueprint, request, jsonify
from db import db, Users
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/', defaults={'user_id': None}, methods=['GET'])
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_users(user_id):
    if user_id:
        user = Users.query.get(user_id)
        if user:
            return jsonify({
                'user_id': user.user_id,
                'is_admin': user.is_admin,
                'email': user.email,
                'full_name': user.full_name
            })
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        users = Users.query.all()
        return jsonify([
            {
                'user_id': u.user_id,
                'is_admin': u.is_admin,
                'email': u.email,
                'full_name': u.full_name
            } for u in users
        ])


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    # Validate required fields
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = Users(
        email=data['email'],
        password_hash=hashed_password,
        full_name=data.get('full_name')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user_id': new_user.user_id, 'email': new_user.email}), 201
@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = Users.query.get_or_404(user_id)
    user.email = data.get('email', user.email)
    # Update password if provided
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    user.full_name = data.get('full_name', user.full_name)
    db.session.commit()
    return jsonify({'user_id': user.user_id, 'email': user.email})

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})