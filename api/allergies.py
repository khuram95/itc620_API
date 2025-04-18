# api/allergies.py
from flask import Blueprint, request, jsonify
from db import db, Allergy

allergies_bp = Blueprint('allergies', __name__)

@allergies_bp.route('/', defaults={'allergy_id': None}, methods=['GET'])
@allergies_bp.route('/<int:allergy_id>', methods=['GET'])
def get_allergies(allergy_id):
    if allergy_id:
        allergy = Allergy.query.get(allergy_id)
        if allergy:
            return jsonify({
                'allergy_id': allergy.allergy_id,
                'name': allergy.name,
                'description': allergy.description,
                'created_at': allergy.created_at,
                'updated_at': allergy.updated_at
            })
        else:
            return jsonify({'error': 'Allergy not found'}), 404
    else:
        allergies = Allergy.query.all()
        return jsonify([
            {
                'allergy_id': a.allergy_id,
                'name': a.name,
                'description': a.description,
                'created_at': a.created_at,
                'updated_at': a.updated_at
            } for a in allergies
        ])
@allergies_bp.route('/', methods=['POST'])
def create_allergy():
    data = request.json
    new_allergy = Allergy(name=data['name'], description=data.get('description'))
    db.session.add(new_allergy)
    db.session.commit()
    return jsonify({'allergy_id': new_allergy.allergy_id, 'name': new_allergy.name}), 201

@allergies_bp.route('/<int:allergy_id>', methods=['PUT'])
def update_allergy(allergy_id):
    data = request.json
    allergy = Allergy.query.get_or_404(allergy_id)
    allergy.name = data.get('name', allergy.name)
    allergy.description = data.get('description', allergy.description)
    db.session.commit()
    return jsonify({'allergy_id': allergy.allergy_id, 'name': allergy.name})

@allergies_bp.route('/<int:allergy_id>', methods=['DELETE'])
def delete_allergy(allergy_id):
    allergy = Allergy.query.get_or_404(allergy_id)
    db.session.delete(allergy)
    db.session.commit()
    return jsonify({'message': 'Allergy deleted successfully'})