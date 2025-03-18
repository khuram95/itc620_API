# api/autocomplete.py
from flask import Blueprint, request, jsonify
import requests
from utils.parser import parse_response

autocomplete_bp = Blueprint('autocomplete', __name__)

# Base URLs for external APIs
AUTOCOMPLETE_URL = "https://www.drugs.com/api/autocomplete/?type=interaction-basic&s={search_params}"
INTERACTIONS_CHECK_URL = "https://www.drugs.com/interactions-check.php?professional=1&drug_list={drug_list}"

@autocomplete_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    search_params = request.args.get("search_params")
    if not search_params:
        return jsonify({"error": "search_params is required"}), 400

    try:
        # Make a request to the external API
        response = requests.get(AUTOCOMPLETE_URL.format(search_params=search_params))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return jsonify(response.json())  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "External API error", "detail": str(e)}), 500

@autocomplete_bp.route('/check_interactions', methods=['GET'])
def check_interactions():
    drug_list = request.args.get("drug_list")
    if not drug_list:
        return jsonify({"error": "drug_list is required"}), 400

    try:
        # Make a request to the external API
        response = requests.get(INTERACTIONS_CHECK_URL.format(drug_list=drug_list))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return jsonify(parse_response(response.text))  # Return the parsed response
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "External API error", "detail": str(e)}), 500