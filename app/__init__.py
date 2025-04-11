from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.models import db
from app.auth.auth import auth  # auth blueprint
from app.routes.main import main  # main blueprint

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "your_secret_key"

    # Initialize CORS to allow requests from your frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    })

    # Initialize Extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(main, url_prefix="/api")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app