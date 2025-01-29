from flask import Blueprint, jsonify
from . import users_bp

@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify({'message': 'Users endpoint'}), 200

# app/api/courses.py
from flask import Blueprint, jsonify
from . import courses_bp

@courses_bp.route('/', methods=['GET'])
def get_courses():
    return jsonify({'message': 'Courses endpoint'}), 200