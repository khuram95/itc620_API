# api/references.py
from flask import Blueprint, request, jsonify
from db import db, Reference

references_bp = Blueprint('references', __name__)

@references_bp.route('/', defaults={'reference_id': None}, methods=['GET'])
@references_bp.route('/<int:reference_id>', methods=['GET'])
def get_references(reference_id):
    if reference_id:
        reference = Reference.query.get(reference_id)
        if reference:
            return jsonify({
                'reference_id': reference.reference_id,
                'title': reference.title,
                'url': reference.url,
                'source_type': reference.source_type,
                'created_at': reference.created_at,
                'updated_at': reference.updated_at
            })
        else:
            return jsonify({'error': 'Reference not found'}), 404
    else:
        references = Reference.query.all()
        return jsonify([
            {
                'reference_id': r.reference_id,
                'title': r.title,
                'url': r.url,
                'source_type': r.source_type,
                'created_at': r.created_at,
                'updated_at': r.updated_at
            } for r in references
        ])
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