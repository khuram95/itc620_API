# api/interactions.py
from flask import Blueprint, request, jsonify
from db import db, DrugDrugInteraction, DrugComplementaryInteraction, DrugFoodInteraction

interactions_bp = Blueprint('interactions', __name__)

# Drug-Drug Interactions
@interactions_bp.route('/drug_drug_interactions', methods=['GET'])
def get_drug_drug_interactions():
    interactions = DrugDrugInteraction.query.all()
    return jsonify([{
        'dd_interaction_id': i.dd_interaction_id,
        'medication1_id': i.medication1_id,
        'medication2_id': i.medication2_id,
        'severity': i.severity,
        'description': i.description,
        'recommendation': i.recommendation
    } for i in interactions])

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