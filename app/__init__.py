from flask import Flask, current_app
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

mongo = PyMongo()
bcrypt = Bcrypt()
jwt_manager = JWTManager()

def check_mongodb_connection():
    try:
        # Get MongoDB URI from app configuration
        mongo_uri = current_app.config['MONGO_URI']
        
        # Attempt to create a connection
        client = MongoClient(mongo_uri)
        
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        
        # Close the connection
        client.close()
        
        print("MongoDB connection successful!")
        return True
    
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error connecting to MongoDB: {e}")
        return False
    
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)

    # Import and register blueprints
    from .api import auth_bp, users_bp, courses_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    with app.app_context():
        if check_mongodb_connection():
            print("Server starting with valid MongoDB connection")
        else:
            print("Warning: MongoDB connection could not be established")

    return app