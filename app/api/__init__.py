from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)
courses_bp = Blueprint('courses', __name__)

from . import auth, users, courses
