# api/references.py
from flask import Blueprint, request, jsonify
from db import db, Reference

references_bp = Blueprint('references', __name__)

@references_bp.route('/', methods=['GET'])
def get_references():
    references = Reference.query.all()
    return jsonify([{'reference_id': r.reference_id, 'title': r.title, 'url': r.url} for r in references])

@references_bp.route('/', methods=['POST'])
def create_reference():
    data = request.json
    new_reference = Reference(title=data['title'], url=data.get('url'), source_type=data.get('source_type'))
    db.session.add(new_reference)
    db.session.commit()
    return jsonify({'reference_id': new_reference.reference_id, 'title': new_reference.title}), 201

@references_bp.route('/<int:reference_id>', methods=['PUT'])
def update_reference(reference_id):
    data = request.json
    reference = Reference.query.get_or_404(reference_id)
    reference.title = data.get('title', reference.title)
    reference.url = data.get('url', reference.url)
    reference.source_type = data.get('source_type', reference.source_type)
    db.session.commit()
    return jsonify({'reference_id': reference.reference_id, 'title': reference.title})

@references_bp.route('/<int:reference_id>', methods=['DELETE'])
def delete_reference(reference_id):
    reference = Reference.query.get_or_404(reference_id)
    db.session.delete(reference)
    db.session.commit()
    return jsonify({'message': 'Reference deleted successfully'})