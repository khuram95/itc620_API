from flask import Blueprint, request, jsonify
from db import db, DrugDrugInteraction, DrugComplementaryInteraction, DrugFoodInteraction, Medication
from sqlalchemy.orm import aliased

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/drug_drug/', defaults={'interaction_id': None,}, methods=['GET'])
@interactions_bp.route('/drug_drug/<int:interaction_id>', methods=['GET'])
def get_interactions_by_medications(interaction_id):
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
    if interaction_id:
        query = query.filter(DrugDrugInteraction.dd_interaction_id == interaction_id)
    
    
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

# Drug-Complementary Interactions
@interactions_bp.route('/drug_complementary_interactions', methods=['GET'])
def get_drug_complementary_interactions():
    interactions = DrugComplementaryInteraction.query.all()
    return jsonify([{
        'dc_interaction_id': i.dc_interaction_id,
        'medication_id': i.medication_id,
        'compl_med_id': i.compl_med_id,
        'severity': i.severity,
        'description': i.description,
        'recommendation': i.recommendation
    } for i in interactions])

# Drug-Food Interactions
@interactions_bp.route('/drug_food_interactions', methods=['GET'])
def get_drug_food_interactions():
    interactions = DrugFoodInteraction.query.all()
    return jsonify([{
        'df_interaction_id': i.df_interaction_id,
        'medication_id': i.medication_id,
        'food_id': i.food_id,
        'severity': i.severity,
        'description': i.description,
        'recommendation': i.recommendation
    } for i in interactions])