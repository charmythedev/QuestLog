from flask import Flask
from .extensions import db, migrate, login_manager, ckeditor, bootstrap
from .auth import auth_bp
from .quests import quests_bp
from .main import main_bp
from .shop import shop_bp
from config import Config
from datetime import datetime
from flask_gravatar import Gravatar

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions FIRST
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    Gravatar(app, size=100, rating="g", default="retro")

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        # Import AFTER db.init_app
        from app.models import User
        return db.session.get(User, int(user_id))

    @app.context_processor
    def inject_date():
        return {"date": datetime.now().year}

    # Import models AFTER db.init_app
    with app.app_context():
        from app import models
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(quests_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp)

    return app
