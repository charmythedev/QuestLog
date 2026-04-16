import os
from datetime import datetime

class Config:
    DATE = datetime.now().year

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
