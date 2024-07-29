from flask import Blueprint, request, jsonify
from models import db, Ride, Group, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import role_required

ride_bp = Blueprint('ride', __name__)

@ride_bp.route('/rides', methods=['POST'])
@jwt_required()
@role_required('driver')
def schedule_ride():
    data = request.get_json()
    new_ride = Ride(
        group_id=data['group_id'],
        date=data['date'],
        time=data['time']
    )
    db.session.add(new_ride)
    db.session.commit()
    return jsonify(message="Ride scheduled"), 201

@ride_bp.route('/rides/<ride_id>/join', methods=['POST'])
@jwt_required()
@role_required('passenger')
def join_ride(ride_id):
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity['id'])
    ride = Ride.query.get(ride_id)
    if ride:
        ride.participants.append(user)
        db.session.commit()
        return jsonify(message="Joined ride"), 200
    return jsonify(message="Ride not found"), 404
