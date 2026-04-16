# app/shop/__init__.py

from flask import Blueprint

shop_bp = Blueprint(
    "shop",
    __name__,
    url_prefix=""   # keep empty so /shop stays /shop
)

from . import routes
