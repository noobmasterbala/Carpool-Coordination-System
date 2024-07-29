from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify
from models import User

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_identity = get_jwt_identity()
            user = User.query.get(user_identity['id'])
            if user.role != role:
                return jsonify(message="Access denied"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
