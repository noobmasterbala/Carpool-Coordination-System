from flask import Blueprint, request, jsonify
from models import db, Group, User
from flask_jwt_extended import jwt_required, get_jwt_identity

group_bp = Blueprint('group', __name__)

@group_bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    new_group = Group(
        name=data['name'],
        schedule=data['schedule'],
        max_capacity=data['max_capacity']
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify(message="Group created"), 201

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
