from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.services import User
from bson import ObjectId

def role_required(role):
    """
    Decorator to enforce role-based access control.

    Args:
        role (str): The required role to access the route.

    Returns:
        func: A wrapped function that enforces role-based access control.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Get user ID from JWT identity
                user_id = get_jwt_identity()

                # Convert user_id to ObjectId and fetch user from the database
                user = User.objects(id=ObjectId(user_id)).first()

                # Check if the user exists and has the required role
                if not user:
                    return jsonify({"message": "User not found"}), 404

                if role not in user.roles:  # Assume `user.roles` is a list of role names (strings)
                    return jsonify({"message": "Forbidden: Insufficient role"}), 403

                # Proceed with the request
                return func(*args, **kwargs)

            except Exception as e:
                return jsonify({"message": f"Internal server error: {str(e)}"}), 500

        return wrapper
    return decorator
