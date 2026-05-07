# app/shop/routes.py

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import shop_bp
from ..forms import ShopForm

from ..models import ShopInventory
from ..shop_methods import restock

@shop_bp.route("/shop", endpoint="shop")
@login_required
def shop():
    # todo: restock shop (every day or so), logic for if a user buys an item (separate function), render shop items in html (loop) (almost)
    user = current_user
    form = ShopForm()

    restock(user)
    shop_inventory = user.shop_inventory


    return render_template("shop.html", user=user, shop_inventory=shop_inventory, form = form)

@shop_bp.route("/buy/<item_id>", methods=["GET", "POST"], endpoint="buy_item")
@login_required
def buy_item(item_id):
    form = ShopForm()
    item = ShopInventory.query.filter_by(id=item_id).first()


    user = current_user

    quantity = int(form.quantity, 1)
    flash(f"{quantity} {item.name} added to inventory.", "success")
    return redirect(url_for("shop"))

    # continue later
    # todo: render shop/ quantity form
    # todo: check if player has enough money/shop has inventory etc.
    #todo buttons for buying in shop
    # todo

