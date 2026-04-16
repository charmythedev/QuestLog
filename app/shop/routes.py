# app/shop/routes.py

from flask import render_template
from flask_login import login_required, current_user

from . import shop_bp


@shop_bp.route("/shop", endpoint="shop")
@login_required
def shop():
    user = current_user
    return render_template("shop.html", user=user)
