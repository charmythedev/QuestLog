# app/shop/routes.py

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import shop_bp
from ..forms import ShopForm
import datetime
from ..models import ShopInventory, Inventory
from ..shop_methods import restock
from app.extensions import db

@shop_bp.route("/shop", endpoint="shop")
@login_required
def shop():
    # todo: restock shop (every day or so), logic for if a user buys an item (separate function), render shop items in html (loop) (almost)
    user = current_user
    form = ShopForm()



    shop_inventory = user.shop_inventory
    now = datetime.datetime.now()
    last_restock =  shop_inventory.last_restock


    if last_restock is None:
        restock(user)
        shop_inventory.last_restock = now
        db.session.commit()

    else:
        delta = now - last_restock
        if delta >= datetime.timedelta(hours=24):
            restock(user)
            shop_inventory.last_restock = now
            db.session.commit()

    return render_template("shop.html", user=user, shop_inventory=shop_inventory, form = form)

@shop_bp.route("/buy/<int:item_id>", methods=["POST"], endpoint="buy_item")
@login_required
def buy_item(item_id):
    form = ShopForm()

    if not form.validate_on_submit():
        return redirect(url_for("shop"))

    user = current_user
    quantity = form.quantity.data

    shop_item = ShopInventory.query.filter_by(id=item_id).first()
    item = shop_item.item

    cost = quantity * item.base_price

    if shop_item.quantity < quantity:
        flash("not enough stock in shop.", "danger")
        return redirect(url_for("shop"))


    if user.current_coins < cost:
        flash("not enough coins.", "danger")
        return redirect(url_for("shop"))

    user.current_coins -= cost

    inv = Inventory.query.filter_by(user_id=user.id,
                                    item_id=item.id
                                    ).first()
    if not inv:
        inv = Inventory(user_id=user.id, item_id=item.id, quantity = 0)
        db.session.add(inv)
    inv.quantity += quantity

    shop_item.quantity -= quantity
    db.session.commit()



    flash(f"{quantity} {item.name} added to inventory.", "success")
    return redirect(url_for("shop"))

    # continue later
    # todo: render shop/ quantity form
    # todo: check if player has enough money/shop has inventory etc.
    #todo: buttons for buying in shop
    # todo: do i need new endpoint? i guess so.

