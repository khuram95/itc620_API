# db.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Allergy(db.Model):
    __tablename__ = 'Allergy'
    allergy_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class ComplementaryMedicine(db.Model):
    __tablename__ = 'ComplementaryMedicine'
    compl_med_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class DrugComplementaryInteraction(db.Model):
    __tablename__ = 'DrugComplementaryInteraction'
    dc_interaction_id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'), nullable=False)
    compl_med_id = db.Column(db.Integer, db.ForeignKey('ComplementaryMedicine.compl_med_id'), nullable=False)
    severity = db.Column(db.String(50))
    description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class DrugDrugInteraction(db.Model):
    __tablename__ = 'DrugDrugInteraction'
    dd_interaction_id = db.Column(db.Integer, primary_key=True)
    medication1_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'), nullable=False)
    medication2_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'), nullable=False)
    severity = db.Column(db.String(50))
    description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class DrugFoodInteraction(db.Model):
    __tablename__ = 'DrugFoodInteraction'
    df_interaction_id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('FoodItem.food_id'), nullable=False)
    severity = db.Column(db.String(50))
    description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class FoodItem(db.Model):
    __tablename__ = 'FoodItem'
    food_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class MedicationAllergy(db.Model):
    __tablename__ = 'MedicationAllergy'
    med_allergy_id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'), nullable=False)
    allergy_id = db.Column(db.Integer, db.ForeignKey('Allergy.allergy_id'), nullable=False)
    notes = db.Column(db.Text)

class MedicationReference(db.Model):
    __tablename__ = 'MedicationReference'
    med_ref_id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'), nullable=False)
    reference_id = db.Column(db.Integer, db.ForeignKey('Reference.reference_id'), nullable=False)

class MedicationSchedule(db.Model):
    __tablename__ = 'MedicationSchedule'
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.medication_id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.ScheduleID'))

    # Relationship definitions
    medication = db.relationship('Medication', back_populates='medication_schedules')
    schedule = db.relationship('Schedules', back_populates='medication_schedules')

class Reference(db.Model):
    __tablename__ = 'Reference'
    reference_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.Text)
    source_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Medication(db.Model):
    __tablename__ = 'medication'
    medication_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    indications = db.Column(db.Text)
    counselling = db.Column(db.Text)
    adverse_effect = db.Column(db.Text)
    practice_points = db.Column(db.Text)
     # Add a relationship to MedicationSchedule
    medication_schedules = db.relationship('MedicationSchedule', back_populates='medication')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Schedules(db.Model):
    __tablename__ = 'schedules'
    ScheduleID = db.Column(db.Integer, primary_key=True)
    ScheduleName = db.Column(db.String(50), nullable=False)
     # Add a relationship to MedicationSchedule
    medication_schedules = db.relationship('MedicationSchedule', back_populates='schedule')
    Description = db.Column(db.Text)
