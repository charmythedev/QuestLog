# app/shop/routes.py

from flask import render_template
from flask_login import login_required, current_user

from . import shop_bp
from ..models import ShopInventory


@shop_bp.route("/shop", endpoint="shop")
@login_required
def shop():
    # todo: restock shop (every day or so), logic for if a user buys an item (separate function), render shop items in html (loop)
    user = current_user
    shop_inventory = ShopInventory.query.all()

    return render_template("shop.html", user=user, shop_inventory=shop_inventory)
