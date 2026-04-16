# app/quests/__init__.py

from flask import Blueprint

quests_bp = Blueprint(
    "quests",
    __name__,
    url_prefix=""   # keep empty so URLs stay the same
)

from . import routes
