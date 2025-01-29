from flask import jsonify, request
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .. import mongo
from . import users_bp
from roles.decorators import role_required  # Import the custom decorator

@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_all_users():
    try:
        users = list(mongo.db.users.find({}, {'password': 0}))
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'faculty'])
def update_user(user_id):
    try:
        user_data = request.json
        update_fields = {key: value for key, value in user_data.items() if key in ['name', 'email']}
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        result = mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_fields})
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_user(user_id):
    try:
        result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
