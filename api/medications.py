# api/medications.py
from flask import Blueprint, request, jsonify
from db import db, Medication
import pdb
medications_bp = Blueprint('medications', __name__)

@medications_bp.route('/', defaults={'medication_id': None}, methods=['GET'])
@medications_bp.route('/<int:medication_id>', methods=['GET'])
def get_medications(medication_id):
    if medication_id:
        medication = Medication.query.get(medication_id)
        if medication:
            return jsonify({
                'medication_id': medication.medication_id,
                'name': medication.name,
                'description': medication.description,
                'indications': medication.indications,
                'counselling': medication.counselling,
                'adverse_effect': medication.adverse_effect,
                'practice_points': medication.practice_points,
                'created_at': medication.created_at.isoformat() if medication.created_at else None,
                'updated_at': medication.updated_at.isoformat() if medication.updated_at else None
            })
        else:
            return jsonify({'error': 'Medication not found'}), 404
    else:
        medications = Medication.query.all()
        return jsonify([
            {
                'medication_id': m.medication_id,
                'name': m.name,
                'description': m.description,
                'indications': m.indications,
                'counselling': m.counselling,
                'adverse_effect': m.adverse_effect,
                'practice_points': m.practice_points,
                'created_at': m.created_at.isoformat() if m.created_at else None,
                'updated_at': m.updated_at.isoformat() if m.updated_at else None
            } for m in medications
        ])

@medications_bp.route('/', methods=['POST'])
def create_medication():
    data = request.json
    new_medication = Medication(
        name=data['name'],
        description=data.get('description'),
        indications=data.get('indications'),
        counselling=data.get('counselling'),
        adverse_effect=data.get('adverse_effect'),
        practice_points=data.get('practice_points')
    )
    db.session.add(new_medication)
    db.session.commit()
    return jsonify({'medication_id': new_medication.medication_id, 'name': new_medication.name}), 201

@medications_bp.route('/<int:medication_id>', methods=['PUT'])
def update_medication(medication_id):
    data = request.json
    medication = Medication.query.get_or_404(medication_id)
    medication.name = data.get('name', medication.name)
    medication.description = data.get('description', medication.description)
    medication.indications = data.get('indications', medication.indications)
    medication.counselling = data.get('counselling', medication.counselling)
    medication.adverse_effect = data.get('adverse_effect', medication.adverse_effect)
    medication.practice_points = data.get('practice_points', medication.practice_points)
    db.session.commit()
    return jsonify({'medication_id': medication.medication_id, 'name': medication.name})

@medications_bp.route('/<int:medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    db.session.delete(medication)
    db.session.commit()
    return jsonify({'message': 'Medication deleted successfully'})