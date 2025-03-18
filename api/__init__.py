# api/__init__.py
from flask import Blueprint
from .allergies import allergies_bp
from .medications import medications_bp
from .interactions import interactions_bp
from .food_items import food_items_bp
from .users import users_bp
from .schedules import schedules_bp
from .references import references_bp
from .autocomplete import autocomplete_bp
from .complementary_medicines import complementary_medicines_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(allergies_bp, url_prefix='/allergies')
api_bp.register_blueprint(medications_bp, url_prefix='/medications')
api_bp.register_blueprint(interactions_bp, url_prefix='/interactions')
api_bp.register_blueprint(food_items_bp, url_prefix='/food_items')
api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(schedules_bp, url_prefix='/schedules')
api_bp.register_blueprint(references_bp, url_prefix='/references')
api_bp.register_blueprint(autocomplete_bp, url_prefix='/')
api_bp.register_blueprint(complementary_medicines_bp, url_prefix='/complementary_medicines')
