from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

# Initialize the database and JWT manager
db = MongoEngine()
jwt_manager = JWTManager()
