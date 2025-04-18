# D:\murodch\Project\app\itc620_API\api\interactions.py

from flask import Blueprint, request, jsonify
from itertools import combinations # <--- IMPORT ADDED
from sqlalchemy import or_, and_ # <--- IMPORT ADDED
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError
# Make sure all necessary models are imported from your db setup
from db import db, DrugDrugInteraction, DrugComplementaryInteraction, DrugFoodInteraction, Medication, ComplementaryMedicine, FoodItem

interactions_bp = Blueprint('interactions', __name__)

# --- Drug-Drug Interactions ---

@interactions_bp.route('/drug_drug/', defaults={'interaction_id': None}, methods=['GET'])
@interactions_bp.route('/drug_drug/<int:interaction_id>', methods=['GET'])
def get_drug_drug_interactions(interaction_id):
    """
    GET Drug-Drug interactions.
    If interaction_id is provided, returns a single interaction.
    Otherwise, returns all interactions.
    Includes medication names via joins.
    """
    med1 = aliased(Medication)
    med2 = aliased(Medication)
    query = db.session.query(
        DrugDrugInteraction.dd_interaction_id,
        DrugDrugInteraction.medication1_id,
        DrugDrugInteraction.medication2_id,
        DrugDrugInteraction.severity,
        DrugDrugInteraction.description,
        DrugDrugInteraction.recommendation,
        # DrugDrugInteraction.created_at, # Uncomment if needed
        # DrugDrugInteraction.updated_at, # Uncomment if needed
        med1.name.label('medication1_name'),
        med2.name.label('medication2_name')
    ).join(med1, med1.medication_id == DrugDrugInteraction.medication1_id) \
     .join(med2, med2.medication_id == DrugDrugInteraction.medication2_id)

    if interaction_id:
        interaction = query.filter(DrugDrugInteraction.dd_interaction_id == interaction_id).first()
        if not interaction:
            return jsonify({'message': 'Interaction not found'}), 404
        result = {
            'dd_interaction_id': interaction.dd_interaction_id,
            'medication1_id': interaction.medication1_id,
            'medication1_name': interaction.medication1_name,
            'medication2_id': interaction.medication2_id,
            'medication2_name': interaction.medication2_name,
            'severity': interaction.severity,
            'description': interaction.description,
            'recommendation': interaction.recommendation
            # Add timestamps if needed
        }
        return jsonify(result)
    else:
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
            # Add timestamps if needed
        } for ddi in interactions]
        return jsonify(result)

@interactions_bp.route('/drug_drug/', methods=['POST'])
def create_drug_drug_interaction():
    """
    POST (Create) a new Drug-Drug interaction.
    Expects JSON data in the request body.
    """
    data = request.get_json()

    if not data or not data.get('medication1_id') or not data.get('medication2_id'):
        return jsonify({'message': 'Missing required fields: medication1_id and medication2_id'}), 400

    # Optional: Validate if medication IDs exist
    med1_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication1_id']).first() is not None
    med2_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication2_id']).first() is not None
    if not med1_exists or not med2_exists:
        return jsonify({'message': 'One or both medication IDs do not exist'}), 400

    new_interaction = DrugDrugInteraction(
        medication1_id=data['medication1_id'],
        medication2_id=data['medication2_id'],
        severity=data.get('severity'),
        description=data.get('description'),
        recommendation=data.get('recommendation')
    )

    try:
        db.session.add(new_interaction)
        db.session.commit()
        # Fetch medication names for the response
        med1 = db.session.get(Medication, new_interaction.medication1_id)
        med2 = db.session.get(Medication, new_interaction.medication2_id)
        response_data = {
            'dd_interaction_id': new_interaction.dd_interaction_id,
            'medication1_id': new_interaction.medication1_id,
            'medication1_name': med1.name if med1 else None,
            'medication2_id': new_interaction.medication2_id,
            'medication2_name': med2.name if med2 else None,
            'severity': new_interaction.severity,
            'description': new_interaction.description,
            'recommendation': new_interaction.recommendation
        }
        return jsonify(response_data), 201 # 201 Created status code
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error', 'error': str(e)}), 409 # Conflict
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@interactions_bp.route('/drug_drug/<int:interaction_id>', methods=['PUT'])
def update_drug_drug_interaction(interaction_id):
    """
    PUT (Update) an existing Drug-Drug interaction by its ID.
    Expects JSON data in the request body.
    """
    interaction = db.session.get(DrugDrugInteraction, interaction_id)
    if not interaction:
        return jsonify({'message': 'Interaction not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided for update'}), 400

    if 'medication1_id' in data:
        med1_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication1_id']).first() is not None
        if not med1_exists:
            return jsonify({'message': f"Medication with ID {data['medication1_id']} not found"}), 400
        interaction.medication1_id = data['medication1_id']
    if 'medication2_id' in data:
        med2_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication2_id']).first() is not None
        if not med2_exists:
            return jsonify({'message': f"Medication with ID {data['medication2_id']} not found"}), 400
        interaction.medication2_id = data['medication2_id']
    if 'severity' in data:
        interaction.severity = data['severity']
    if 'description' in data:
        interaction.description = data['description']
    if 'recommendation' in data:
        interaction.recommendation = data['recommendation']

    try:
        db.session.commit()
        med1 = db.session.get(Medication, interaction.medication1_id)
        med2 = db.session.get(Medication, interaction.medication2_id)
        response_data = {
            'dd_interaction_id': interaction.dd_interaction_id,
            'medication1_id': interaction.medication1_id,
            'medication1_name': med1.name if med1 else None,
            'medication2_id': interaction.medication2_id,
            'medication2_name': med2.name if med2 else None,
            'severity': interaction.severity,
            'description': interaction.description,
            'recommendation': interaction.recommendation
        }
        return jsonify(response_data), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error during update', 'error': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred during update', 'error': str(e)}), 500


# --- Drug-Complementary Interactions ---

@interactions_bp.route('/drug_complementary/', defaults={'interaction_id': None}, methods=['GET'])
@interactions_bp.route('/drug_complementary/<int:interaction_id>', methods=['GET'])
def get_drug_complementary_interactions(interaction_id):
    """ GET Drug-Complementary interactions """
    query = db.session.query(
        DrugComplementaryInteraction,
        Medication.name.label('medication_name'),
        ComplementaryMedicine.name.label('complementary_medicine_name')
    ).join(Medication, Medication.medication_id == DrugComplementaryInteraction.medication_id) \
     .join(ComplementaryMedicine, ComplementaryMedicine.compl_med_id == DrugComplementaryInteraction.compl_med_id)

    if interaction_id:
        result = query.filter(DrugComplementaryInteraction.dc_interaction_id == interaction_id).first()
        if not result:
            return jsonify({'message': 'Interaction not found'}), 404
        i, med_name, compl_med_name = result
        response = {
            'dc_interaction_id': i.dc_interaction_id,
            'medication_id': i.medication_id,
            'medication_name': med_name,
            'compl_med_id': i.compl_med_id,
            'complementary_medicine_name': compl_med_name,
            'severity': i.severity,
            'description': i.description,
            'recommendation': i.recommendation
        }
        return jsonify(response)
    else:
        interactions = query.all()
        result = [{
            'dc_interaction_id': i.dc_interaction_id,
            'medication_id': i.medication_id,
            'medication_name': med_name,
            'compl_med_id': i.compl_med_id,
            'complementary_medicine_name': compl_med_name,
            'severity': i.severity,
            'description': i.description,
            'recommendation': i.recommendation
        } for i, med_name, compl_med_name in interactions]
        return jsonify(result)

@interactions_bp.route('/drug_complementary/', methods=['POST'])
def create_drug_complementary_interaction():
    """ POST (Create) a new Drug-Complementary interaction """
    data = request.get_json()
    if not data or not data.get('medication_id') or not data.get('compl_med_id'):
        return jsonify({'message': 'Missing required fields: medication_id and compl_med_id'}), 400

    med_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication_id']).first() is not None
    compl_exists = db.session.query(ComplementaryMedicine.compl_med_id).filter_by(compl_med_id=data['compl_med_id']).first() is not None
    if not med_exists or not compl_exists:
        return jsonify({'message': 'Medication or Complementary Medicine ID does not exist'}), 400

    new_interaction = DrugComplementaryInteraction(
        medication_id=data['medication_id'],
        compl_med_id=data['compl_med_id'],
        severity=data.get('severity'),
        description=data.get('description'),
        recommendation=data.get('recommendation')
    )
    try:
        db.session.add(new_interaction)
        db.session.commit()
        med = db.session.get(Medication, new_interaction.medication_id)
        compl = db.session.get(ComplementaryMedicine, new_interaction.compl_med_id)
        response_data = {
            'dc_interaction_id': new_interaction.dc_interaction_id,
            'medication_id': new_interaction.medication_id,
            'medication_name': med.name if med else None,
            'compl_med_id': new_interaction.compl_med_id,
            'complementary_medicine_name': compl.name if compl else None,
            'severity': new_interaction.severity,
            'description': new_interaction.description,
            'recommendation': new_interaction.recommendation
        }
        return jsonify(response_data), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error', 'error': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@interactions_bp.route('/drug_complementary/<int:interaction_id>', methods=['PUT'])
def update_drug_complementary_interaction(interaction_id):
    """ PUT (Update) an existing Drug-Complementary interaction """
    interaction = db.session.get(DrugComplementaryInteraction, interaction_id)
    if not interaction:
        return jsonify({'message': 'Interaction not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided for update'}), 400

    if 'medication_id' in data:
        med_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication_id']).first() is not None
        if not med_exists: return jsonify({'message': f"Medication ID {data['medication_id']} not found"}), 400
        interaction.medication_id = data['medication_id']
    if 'compl_med_id' in data:
        compl_exists = db.session.query(ComplementaryMedicine.compl_med_id).filter_by(compl_med_id=data['compl_med_id']).first() is not None
        if not compl_exists: return jsonify({'message': f"Complementary Medicine ID {data['compl_med_id']} not found"}), 400
        interaction.compl_med_id = data['compl_med_id']
    if 'severity' in data:
        interaction.severity = data['severity']
    if 'description' in data:
        interaction.description = data['description']
    if 'recommendation' in data:
        interaction.recommendation = data['recommendation']

    try:
        db.session.commit()
        med = db.session.get(Medication, interaction.medication_id)
        compl = db.session.get(ComplementaryMedicine, interaction.compl_med_id)
        response_data = {
            'dc_interaction_id': interaction.dc_interaction_id,
            'medication_id': interaction.medication_id,
            'medication_name': med.name if med else None,
            'compl_med_id': interaction.compl_med_id,
            'complementary_medicine_name': compl.name if compl else None,
            'severity': interaction.severity,
            'description': interaction.description,
            'recommendation': interaction.recommendation
        }
        return jsonify(response_data), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error during update', 'error': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred during update', 'error': str(e)}), 500


# --- Drug-Food Interactions ---

@interactions_bp.route('/drug_food/', defaults={'interaction_id': None}, methods=['GET'])
@interactions_bp.route('/drug_food/<int:interaction_id>', methods=['GET'])
def get_drug_food_interactions(interaction_id):
    """ GET Drug-Food interactions """
    query = db.session.query(
        DrugFoodInteraction,
        Medication.name.label('medication_name'),
        FoodItem.name.label('food_name')
    ).join(Medication, Medication.medication_id == DrugFoodInteraction.medication_id) \
     .join(FoodItem, FoodItem.food_id == DrugFoodInteraction.food_id)

    if interaction_id:
        result = query.filter(DrugFoodInteraction.df_interaction_id == interaction_id).first()
        if not result:
            return jsonify({'message': 'Interaction not found'}), 404
        i, med_name, food_name = result
        response = {
            'df_interaction_id': i.df_interaction_id,
            'medication_id': i.medication_id,
            'medication_name': med_name,
            'food_id': i.food_id,
            'food_name': food_name,
            'severity': i.severity,
            'description': i.description,
            'recommendation': i.recommendation
        }
        return jsonify(response)
    else:
        interactions = query.all()
        result = [{
            'df_interaction_id': i.df_interaction_id,
            'medication_id': i.medication_id,
            'medication_name': med_name,
            'food_id': i.food_id,
            'food_name': food_name,
            'severity': i.severity,
            'description': i.description,
            'recommendation': i.recommendation
        } for i, med_name, food_name in interactions]
        return jsonify(result)

@interactions_bp.route('/drug_food/', methods=['POST'])
def create_drug_food_interaction():
    """ POST (Create) a new Drug-Food interaction """
    data = request.get_json()
    if not data or not data.get('medication_id') or not data.get('food_id'):
        return jsonify({'message': 'Missing required fields: medication_id and food_id'}), 400

    med_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication_id']).first() is not None
    food_exists = db.session.query(FoodItem.food_id).filter_by(food_id=data['food_id']).first() is not None
    if not med_exists or not food_exists:
        return jsonify({'message': 'Medication or Food ID does not exist'}), 400

    new_interaction = DrugFoodInteraction(
        medication_id=data['medication_id'],
        food_id=data['food_id'],
        severity=data.get('severity'),
        description=data.get('description'),
        recommendation=data.get('recommendation')
    )
    try:
        db.session.add(new_interaction)
        db.session.commit()
        med = db.session.get(Medication, new_interaction.medication_id)
        food = db.session.get(FoodItem, new_interaction.food_id)
        response_data = {
            'df_interaction_id': new_interaction.df_interaction_id,
            'medication_id': new_interaction.medication_id,
            'medication_name': med.name if med else None,
            'food_id': new_interaction.food_id,
            'food_name': food.name if food else None,
            'severity': new_interaction.severity,
            'description': new_interaction.description,
            'recommendation': new_interaction.recommendation
        }
        return jsonify(response_data), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error', 'error': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@interactions_bp.route('/drug_food/<int:interaction_id>', methods=['PUT'])
def update_drug_food_interaction(interaction_id):
    """ PUT (Update) an existing Drug-Food interaction """
    interaction = db.session.get(DrugFoodInteraction, interaction_id)
    if not interaction:
        return jsonify({'message': 'Interaction not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided for update'}), 400

    if 'medication_id' in data:
        med_exists = db.session.query(Medication.medication_id).filter_by(medication_id=data['medication_id']).first() is not None
        if not med_exists: return jsonify({'message': f"Medication ID {data['medication_id']} not found"}), 400
        interaction.medication_id = data['medication_id']
    if 'food_id' in data:
        food_exists = db.session.query(FoodItem.food_id).filter_by(food_id=data['food_id']).first() is not None
        if not food_exists: return jsonify({'message': f"Food ID {data['food_id']} not found"}), 400
        interaction.food_id = data['food_id']
    if 'severity' in data:
        interaction.severity = data['severity']
    if 'description' in data:
        interaction.description = data['description']
    if 'recommendation' in data:
        interaction.recommendation = data['recommendation']

    try:
        db.session.commit()
        med = db.session.get(Medication, interaction.medication_id)
        food = db.session.get(FoodItem, interaction.food_id)
        response_data = {
            'df_interaction_id': interaction.df_interaction_id,
            'medication_id': interaction.medication_id,
            'medication_name': med.name if med else None,
            'food_id': interaction.food_id,
            'food_name': food.name if food else None,
            'severity': interaction.severity,
            'description': interaction.description,
            'recommendation': interaction.recommendation
        }
        return jsonify(response_data), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error during update', 'error': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred during update', 'error': str(e)}), 500


# --- Interaction Check Endpoint ---
@interactions_bp.route('/check', methods=['POST'])
def check_interactions():
    """
    Checks for interactions between provided lists of drug, food,
    and complementary medicine IDs.
    Expects JSON body: {"drug_ids": [], "food_ids": [], "comp_ids": []}
    """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing request body'}), 400

    drug_ids = data.get('drug_ids', [])
    food_ids = data.get('food_ids', [])
    comp_ids = data.get('comp_ids', [])

    # Ensure IDs are integers (or appropriate type for your DB)
    try:
        # Filter out potential None or empty string values before converting
        drug_ids = [int(id_str) for id_str in drug_ids if id_str]
        food_ids = [int(id_str) for id_str in food_ids if id_str]
        comp_ids = [int(id_str) for id_str in comp_ids if id_str]
    except ValueError:
        return jsonify({'message': 'Invalid ID format. IDs must be convertible to integers.'}), 400
    except TypeError:
         return jsonify({'message': 'Invalid ID format. IDs must be provided as strings or numbers.'}), 400


    found_interactions = {
        'drug_drug': [],
        'drug_food': [],
        'drug_complementary': []
    }

    # --- 1. Check Drug-Drug Interactions ---
    if len(drug_ids) >= 2:
        try:
            med1_alias = aliased(Medication)
            med2_alias = aliased(Medication)

            # Generate all unique pairs of drug IDs
            drug_pairs = list(combinations(drug_ids, 2)) # combinations is now imported

            if drug_pairs: # Only query if there are pairs to check
                # Create filter conditions for each pair
                # Assuming interactions are stored consistently (med1_id < med2_id) or symmetrically
                # This version handles both (med1, med2) and (med2, med1) storage
                conditions = or_(*[
                    or_(
                         and_(DrugDrugInteraction.medication1_id == p[0], DrugDrugInteraction.medication2_id == p[1]),
                         and_(DrugDrugInteraction.medication1_id == p[1], DrugDrugInteraction.medication2_id == p[0])
                     ) for p in drug_pairs
                ])

                # If you store consistently with med1_id < med2_id, use this simpler condition:
                # conditions = or_(*[
                #     and_(
                #         DrugDrugInteraction.medication1_id == min(p[0], p[1]),
                #         DrugDrugInteraction.medication2_id == max(p[0], p[1])
                #     ) for p in drug_pairs
                # ])

                dd_interactions = db.session.query(
                    DrugDrugInteraction.dd_interaction_id,
                    DrugDrugInteraction.medication1_id,
                    DrugDrugInteraction.medication2_id,
                    DrugDrugInteraction.severity,
                    DrugDrugInteraction.description,
                    DrugDrugInteraction.recommendation,
                    med1_alias.name.label('medication1_name'),
                    med2_alias.name.label('medication2_name')
                ).join(med1_alias, med1_alias.medication_id == DrugDrugInteraction.medication1_id) \
                 .join(med2_alias, med2_alias.medication_id == DrugDrugInteraction.medication2_id) \
                 .filter(conditions) \
                 .all()

                found_interactions['drug_drug'] = [{
                    'dd_interaction_id': i.dd_interaction_id,
                    'medication1_id': i.medication1_id,
                    'medication1_name': i.medication1_name,
                    'medication2_id': i.medication2_id,
                    'medication2_name': i.medication2_name,
                    'severity': i.severity,
                    'description': i.description,
                    'recommendation': i.recommendation
                } for i in dd_interactions]
        except Exception as e:
             print(f"Error during drug-drug interaction query: {e}") # Log error
             # Optionally return a 500 error or just continue

    # --- 2. Check Drug-Food Interactions ---
    if drug_ids and food_ids:
        try:
            med_alias = aliased(Medication)
            food_alias = aliased(FoodItem)
            df_interactions = db.session.query(
                DrugFoodInteraction, # Select the whole object
                med_alias.name.label('medication_name'),
                food_alias.name.label('food_name')
            ).join(med_alias, med_alias.medication_id == DrugFoodInteraction.medication_id) \
             .join(food_alias, food_alias.food_id == DrugFoodInteraction.food_id) \
             .filter(
                 DrugFoodInteraction.medication_id.in_(drug_ids),
                 DrugFoodInteraction.food_id.in_(food_ids)
             ).all()

            # Access attributes directly from the interaction object (i[0])
            found_interactions['drug_food'] = [{
                'df_interaction_id': i[0].df_interaction_id,
                'medication_id': i[0].medication_id,
                'medication_name': i.medication_name, # Name comes from the labeled column
                'food_id': i[0].food_id,
                'food_name': i.food_name, # Name comes from the labeled column
                'severity': i[0].severity,
                'description': i[0].description,
                'recommendation': i[0].recommendation
            } for i in df_interactions]
        except Exception as e:
            print(f"Error during drug-food interaction query: {e}") # Log error

    # --- 3. Check Drug-Complementary Interactions ---
    if drug_ids and comp_ids:
        try:
            med_alias = aliased(Medication)
            comp_alias = aliased(ComplementaryMedicine)
            dc_interactions = db.session.query(
                DrugComplementaryInteraction, # Select the whole object
                med_alias.name.label('medication_name'),
                comp_alias.name.label('complementary_medicine_name')
            ).join(med_alias, med_alias.medication_id == DrugComplementaryInteraction.medication_id) \
             .join(comp_alias, comp_alias.compl_med_id == DrugComplementaryInteraction.compl_med_id) \
             .filter(
                 DrugComplementaryInteraction.medication_id.in_(drug_ids),
                 DrugComplementaryInteraction.compl_med_id.in_(comp_ids)
             ).all()

            # Access attributes directly from the interaction object (i[0])
            found_interactions['drug_complementary'] = [{
                'dc_interaction_id': i[0].dc_interaction_id,
                'medication_id': i[0].medication_id,
                'medication_name': i.medication_name, # Name comes from the labeled column
                'compl_med_id': i[0].compl_med_id,
                'complementary_medicine_name': i.complementary_medicine_name, # Name comes from labeled column
                'severity': i[0].severity,
                'description': i[0].description,
                'recommendation': i[0].recommendation
            } for i in dc_interactions]
        except Exception as e:
            print(f"Error during drug-comp interaction query: {e}") # Log error

    # Return all found interactions
    return jsonify(found_interactions), 200