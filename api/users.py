# api/users.py
from flask import Blueprint, request, jsonify
from db import db, Users

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([{'user_id': u.user_id, 'email': u.email, 'full_name': u.full_name} for u in users])

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    new_user = Users(email=data['email'], password_hash=data['password_hash'], full_name=data.get('full_name'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user_id': new_user.user_id, 'email': new_user.email}), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = Users.query.get_or_404(user_id)
    user.email = data.get('email', user.email)
    user.password_hash = data.get('password_hash', user.password_hash)
    user.full_name = data.get('full_name', user.full_name)
    db.session.commit()
    return jsonify({'user_id': user.user_id, 'email': user.email})

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})