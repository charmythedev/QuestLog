# app/auth/__init__.py

from flask import Blueprint

main_bp = Blueprint(
    "main",        # blueprint name
    __name__,      # module name
    url_prefix=""  # keep empty so your routes stay the same
)

from . import routes   # this imports routes.py so the routes register
