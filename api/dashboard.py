# api/dashboard.py
from flask import Blueprint, request, jsonify
from db import (Reference, Medication, Allergy, ComplementaryMedicine, FoodItem, Users, Schedules)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def get_dashboard_info():
    # Get counts for all models
    dashboard_data = {
        'medications': Medication.query.count(),
        'allergies': Allergy.query.count(),
        'complementary_medicines': ComplementaryMedicine.query.count(),
        'food_items': FoodItem.query.count(),
        'references': Reference.query.count(),
        'users': Users.query.count(),
        'schedules': Schedules.query.count()
    }

    return jsonify(dashboard_data)