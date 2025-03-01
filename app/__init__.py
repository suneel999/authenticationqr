from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Configure LoginManager
    login_manager.login_view = 'auth.login'  # Set the login view
    login_manager.login_message_category = 'info'  # Optional: Set a message category for flashed messages

    # Import and register Blueprints
    from app.routes import main_routes, auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    return app