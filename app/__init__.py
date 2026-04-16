from flask import Flask
from .extensions import db, migrate, login_manager, ckeditor, bootstrap
from .auth import auth_bp
from .quests import quests_bp
from .main import main_bp
from .shop import shop_bp
from app.models import User
from config import Config
from datetime import datetime
from flask_gravatar import Gravatar
from sqlalchemy.exc import OperationalError

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    Gravatar(app, size=100, rating="g", default="retro")

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except OperationalError:
            db.session.rollback()
            return None



    @app.context_processor
    def inject_date():
        return {"date": datetime.now().year}


    with app.app_context():
        from app import models
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(quests_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp)

    return app
