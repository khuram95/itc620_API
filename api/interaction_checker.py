from flask import Blueprint, request, jsonify
from db import db, DrugDrugInteraction, DrugComplementaryInteraction, DrugFoodInteraction, Medication
from sqlalchemy.orm import aliased

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/drug_drug/', defaults={'med1_id': None, 'med2_id': None}, methods=['GET'])
@interactions_bp.route('/drug_drug/<int:med1_id>/<int:med2_id>', methods=['GET'])
def get_interactions_by_medications(med1_id, med2_id):
    med1 = aliased(Medication)
    med2 = aliased(Medication)

    query = db.session.query(
        DrugDrugInteraction.dd_interaction_id,
        DrugDrugInteraction.medication1_id,
        DrugDrugInteraction.medication2_id,
        DrugDrugInteraction.severity,
        DrugDrugInteraction.description,
        DrugDrugInteraction.recommendation,
        med1.name.label('medication1_name'),
        med2.name.label('medication2_name')
    ).join(med1, med1.medication_id == DrugDrugInteraction.medication1_id) \
     .join(med2, med2.medication_id == DrugDrugInteraction.medication2_id)
    
    if med1_id and med2_id:
        query = query.filter(
            ((DrugDrugInteraction.medication1_id == med1_id) & (DrugDrugInteraction.medication2_id == med2_id)) |
            ((DrugDrugInteraction.medication1_id == med2_id) & (DrugDrugInteraction.medication2_id == med1_id))
        )
    
    interactions = query.all()
    result = [{
        'dd_interaction_id': ddi.dd_interaction_id,
        'medication1_id': ddi.medication1_id,
        'medication1_name': ddi.medication1_name,
        'medication2_id': ddi.medication2_id,
        'medication2_name': ddi.medication2_name,
        'severity': ddi.severity,
        'description': ddi.description,
        'recommendation': ddi.recommendation
    } for ddi in interactions]

    return jsonify(result)