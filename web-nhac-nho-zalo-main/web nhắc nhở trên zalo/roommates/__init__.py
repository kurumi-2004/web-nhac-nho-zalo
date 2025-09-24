from flask import Blueprint

roommates = Blueprint('roommates', __name__)

from . import views
from flask import Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Create Blueprint
roommates = Blueprint('roommates', __name__)

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import views after Blueprint creation to avoid circular imports
from . import views, models

def init_app(app):
    """Initialize the application with extensions"""
    db.init_app(app)
    login_manager.init_app(app)
