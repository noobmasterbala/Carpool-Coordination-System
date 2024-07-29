from flask import Blueprint, request, jsonify
from models import db, Group, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import role_required

group_bp = Blueprint('group', __name__)

@group_bp.route('/groups', methods=['POST'])
@jwt_required()
@role_required('driver')
def create_group():
    data = request.get_json()
    user_identity = get_jwt_identity()
    new_group = Group(
        name=data['name'],
        schedule=data['schedule'],
        max_capacity=data['max_capacity'],
        created_by=user_identity['id']  # Store the driver's ID
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify(message="Group created"), 201

@group_bp.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    groups = Group.query.all()
    group_list = []
    for group in groups:
        group_data = {
            'id': str(group.id),
            'name': group.name,
            'schedule': group.schedule,
            'max_capacity': group.max_capacity,
            'members': [{'id': str(member.id), 'name': member.name, 'email': member.email} for member in group.members]
        }
        group_list.append(group_data)
    return jsonify(group_list), 200

@group_bp.route('/groups/<group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity['id'])
    group = Group.query.get(group_id)
    if group and len(group.members) < group.max_capacity:
        group.members.append(user)
        db.session.commit()
        return jsonify(message="Joined group"), 200
    return jsonify(message="Group is full or not found"), 400

@group_bp.route('/groups/<group_id>', methods=['DELETE'])
@jwt_required()
@role_required('driver')
def delete_group(group_id):
    user_identity = get_jwt_identity()
    group = Group.query.get(group_id)
    
    if not group:
        return jsonify(message="Group not found"), 404

    if group.created_by != user_identity['id']:
        return jsonify(message="You are not authorized to delete this group"), 403

    db.session.delete(group)
    db.session.commit()
    return jsonify(message="Group deleted"), 200
