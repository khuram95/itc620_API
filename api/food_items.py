# api/food_items.py
from flask import Blueprint, request, jsonify
from db import db, FoodItem

food_items_bp = Blueprint('food_items', __name__)

@food_items_bp.route('/', methods=['GET'])
def get_food_items():
    food_items = FoodItem.query.all()
    return jsonify([{'food_id': f.food_id, 'name': f.name, 'description': f.description} for f in food_items])

@food_items_bp.route('/', methods=['POST'])
def create_food_item():
    data = request.json
    new_food_item = FoodItem(name=data['name'], description=data.get('description'))
    db.session.add(new_food_item)
    db.session.commit()
    return jsonify({'food_id': new_food_item.food_id, 'name': new_food_item.name}), 201

@food_items_bp.route('/<int:food_id>', methods=['PUT'])
def update_food_item(food_id):
    data = request.json
    food_item = FoodItem.query.get_or_404(food_id)
    food_item.name = data.get('name', food_item.name)
    food_item.description = data.get('description', food_item.description)
    db.session.commit()
    return jsonify({'food_id': food_item.food_id, 'name': food_item.name})

@food_items_bp.route('/<int:food_id>', methods=['DELETE'])
def delete_food_item(food_id):
    food_item = FoodItem.query.get_or_404(food_id)
    db.session.delete(food_item)
    db.session.commit()
    return jsonify({'message': 'Food item deleted successfully'})