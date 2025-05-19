# api/medications.py
from flask import Blueprint, request, jsonify
from db import db, Medication, MedicationSchedule, Reference
import pdb
from sqlalchemy.orm import joinedload

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
                'reference_url': [ref.url for ref in medication.reference],
                'indications': medication.indications,
                'counselling': medication.counselling,
                'adverse_effect': medication.adverse_effect,
                'practice_points': medication.practice_points,
                'schedules': [link.schedule.ScheduleID for link in medication.medication_schedules],
                'allergies': [link.allergy.description for link in medication.medication_allergy],
                'created_at': medication.created_at.isoformat() if medication.created_at else None,
                'updated_at': medication.updated_at.isoformat() if medication.updated_at else None
            })
        else:
            return jsonify({'error': 'Medication not found'}), 404
    else:
        # medications = Medication.query.all()
        medications = Medication.query.options(
                        joinedload(Medication.medication_schedules).joinedload(MedicationSchedule.schedule),
                        joinedload(Medication.reference)
                    ).all()

        return jsonify([
            {
                'medication_id': m.medication_id,
                'name': m.name,
                'description': m.description,
                'reference_url': [ref.url for ref in m.reference],
                'indications': m.indications,
                'counselling': m.counselling,
                'adverse_effect': m.adverse_effect,
                'practice_points': m.practice_points,
                'schedules': [link.schedule.ScheduleID for link in m.medication_schedules],
                'allergies': [link.allergy.description for link in medication.medication_allergy],
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
    db.session.commit() # Commit first to generate medication_id

    # Optional: Add schedules if provided
    if 'schedules' in data:
        for schedule_id in data['schedules']:
            link = MedicationSchedule(medication_id=new_medication.medication_id, schedule_id=schedule_id)
            db.session.add(link)
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

    # Optional: Update schedules if provided
    if 'schedules' in data:
        # Clear existing links
        MedicationSchedule.query.filter_by(medication_id=medication.medication_id).delete()

        # Add new ones
        for schedule_id in data['schedules']:
            new_link = MedicationSchedule(medication_id=medication.medication_id, schedule_id=schedule_id)
            db.session.add(new_link)

    db.session.commit()
    return jsonify({'medication_id': medication.medication_id, 'name': medication.name})

@medications_bp.route('/<int:medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    db.session.delete(medication)
    db.session.commit()
    return jsonify({'message': 'Medication deleted successfully'})