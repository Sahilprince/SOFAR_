from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from .. import bcrypt, mongo
from ..schemas.user_schemas import UserCreateDTO, AdminCreateDTO  
from . import auth_bp

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        user_data = UserCreateDTO(**request.json)
        
        # Check if user exists
        existing_user = mongo.db.users.find_one({'email': user_data.email})
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(user_data.password).decode('utf-8')
        
        # Insert user with static role 'student'
        user = {
            'email': user_data.email,
            'password': hashed_password,
            'name': user_data.name,
            'role': 'student'  # Static role
        }
        mongo.db.users.insert_one(user)

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        # Find the user in the database
        user = mongo.db.users.find_one({'email': email, 'role': 'student'})  # Ensure only students can log in here
        if user and bcrypt.check_password_hash(user['password'], password):
            # Create JWT token
            access_token = create_access_token(identity=str(user['_id']), expires_delta=timedelta(days=2))
            
            # Set the JWT token as a cookie
            response = make_response(jsonify({'message': 'Login successful'}), 200)
            response.set_cookie(
                'access_token_cookie',
                access_token,
                max_age=2 * 24 * 60 * 60,  # 2 days in seconds
                httponly=True,  # Secure the cookie to HTTP only
                samesite='Lax'
            )
            return response
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Clear the cookie to log out the user
        response = make_response(jsonify({'message': 'Logout successful'}), 200)
        response.delete_cookie('access_token_cookie')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------- Admin Routes -------------------

@auth_bp.route('/ganesha@2024/admin/signup', methods=['POST'])
def create_admin():
    try:
        admin_data = AdminCreateDTO(**request.json)
        
        # Check if admin exists
        existing_admin = mongo.db.users.find_one({'email': admin_data.email, 'role': 'admin'})
        if existing_admin:
            return jsonify({'error': 'Admin already exists'}), 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(admin_data.password).decode('utf-8')
        
        # Insert admin with static role 'admin'
        admin = {
            'name': admin_data.name,
            'email': admin_data.email,
            'password': hashed_password,
            'phone_number': admin_data.phone_number,
            'role': 'admin'
        }
        mongo.db.users.insert_one(admin)

        return jsonify({'message': 'Admin created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/ganesha@2024/admin/login', methods=['POST'])
def admin_login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        # Find admin in the database
        admin = mongo.db.users.find_one({'email': email, 'role': 'admin'})
        if admin and bcrypt.check_password_hash(admin['password'], password):
            # Create JWT token for admin
            access_token = create_access_token(identity=str(admin['_id']), expires_delta=timedelta(days=2))
            
            # Set the JWT token as a cookie
            response = make_response(jsonify({'message': 'Admin login successful'}), 200)
            response.set_cookie(
                'access_token_cookie',
                access_token,
                max_age=2 * 24 * 60 * 60,  # 2 days in seconds
                httponly=True,
                samesite='Lax'
            )
            return response

        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400