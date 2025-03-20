# api/schedules.py
from flask import Blueprint, request, jsonify
from db import db, Schedules

schedules_bp = Blueprint('schedules', __name__)

@schedules_bp.route('/', defaults={'schedule_id': None}, methods=['GET'])
@schedules_bp.route('/<int:schedule_id>', methods=['GET'])
def get_schedules(schedule_id):
    if schedule_id:
        schedule = Schedules.query.get(schedule_id)
        if schedule:
            return jsonify({
                'ScheduleID': schedule.ScheduleID,
                'ScheduleName': schedule.ScheduleName,
                'Description': schedule.Description
            })
        else:
            return jsonify({'error': 'Schedule not found'}), 404
    else:
        schedules = Schedules.query.all()
        return jsonify([
            {
                'ScheduleID': s.ScheduleID,
                'ScheduleName': s.ScheduleName,
                'Description': s.Description
            } for s in schedules
        ])

@schedules_bp.route('/', methods=['POST'])
def create_schedule():
    data = request.json
    new_schedule = Schedules(ScheduleName=data['ScheduleName'], Description=data.get('Description'))
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({'ScheduleID': new_schedule.ScheduleID, 'ScheduleName': new_schedule.ScheduleName}), 201

@schedules_bp.route('/<int:ScheduleID>', methods=['PUT'])
def update_schedule(ScheduleID):
    data = request.json
    schedule = Schedules.query.get_or_404(ScheduleID)
    schedule.ScheduleName = data.get('ScheduleName', schedule.ScheduleName)
    schedule.Description = data.get('Description', schedule.Description)
    db.session.commit()
    return jsonify({'ScheduleID': schedule.ScheduleID, 'ScheduleName': schedule.ScheduleName})

@schedules_bp.route('/<int:ScheduleID>', methods=['DELETE'])
def delete_schedule(ScheduleID):
    schedule = Schedules.query.get_or_404(ScheduleID)
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule deleted successfully'})