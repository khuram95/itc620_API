# api/complementary_medicines.py
from flask import Blueprint, request, jsonify
from db import db, ComplementaryMedicine

complementary_medicines_bp = Blueprint('complementary_medicines', __name__)

@complementary_medicines_bp.route('/', defaults={'compl_med_id': None}, methods=['GET'])
@complementary_medicines_bp.route('/<int:compl_med_id>', methods=['GET'])
def get_complementary_medicines(compl_med_id):
    if compl_med_id:
        complementary_medicine = ComplementaryMedicine.query.get(compl_med_id)
        if complementary_medicine:
            return jsonify({
                'compl_med_id': complementary_medicine.compl_med_id,
                'name': complementary_medicine.name,
                'description': complementary_medicine.description
            })
        else:
            return jsonify({'error': 'Complementary medicine not found'}), 404
    else:
        complementary_medicines = ComplementaryMedicine.query.all()
        return jsonify([
            {
                'compl_med_id': cm.compl_med_id,
                'name': cm.name,
                'description': cm.description,
                'created_at': cm.created_at,
                'updated_at': cm.updated_at
            } for cm in complementary_medicines
        ])
    
    
@complementary_medicines_bp.route('/', methods=['POST'])
def create_complementary_medicine():
    data = request.json
    new_complementary_medicine = ComplementaryMedicine(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(new_complementary_medicine)
    db.session.commit()
    return jsonify({
        'compl_med_id': new_complementary_medicine.compl_med_id,
        'name': new_complementary_medicine.name
    }), 201

@complementary_medicines_bp.route('/<int:compl_med_id>', methods=['PUT'])
def update_complementary_medicine(compl_med_id):
    data = request.json
    complementary_medicine = ComplementaryMedicine.query.get_or_404(compl_med_id)
    complementary_medicine.name = data.get('name', complementary_medicine.name)
    complementary_medicine.description = data.get('description', complementary_medicine.description)
    db.session.commit()
    return jsonify({
        'compl_med_id': complementary_medicine.compl_med_id,
        'name': complementary_medicine.name
    })

@complementary_medicines_bp.route('/<int:compl_med_id>', methods=['DELETE'])
def delete_complementary_medicine(compl_med_id):
    complementary_medicine = ComplementaryMedicine.query.get_or_404(compl_med_id)
    db.session.delete(complementary_medicine)
    db.session.commit()
    return jsonify({'message': 'Complementary medicine deleted successfully'})