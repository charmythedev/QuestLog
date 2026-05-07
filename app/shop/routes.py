# app/shop/routes.py

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..leveling import multiplier

from . import shop_bp
from ..forms import ShopForm
import datetime
from app.models import (
    ShopItem,
    Inventory,
    InventoryItem,
    Item
)

from ..shop_methods import restock_shop, seed_items, seed_shop_for_user
from app.extensions import db

@shop_bp.route("/shop", endpoint="shop")
@login_required
def shop():
    user = current_user
    form = ShopForm()
    now = datetime.datetime.now()
    seed_items()
    # Ensure the user has a shop
    if user.shop is None:

        seed_shop_for_user(user)

    shop = user.shop

    # Restock if needed
    if shop.last_restock is None:
        restock_shop(shop)
        shop.last_restock = now
        db.session.commit()

    else:
        delta = now - shop.last_restock
        if delta >= datetime.timedelta(hours=24):
            restock_shop(shop)
            shop.last_restock = now
            db.session.commit()

    return render_template("shop.html", shop=shop, form=form)
@shop_bp.route("/buy/<int:shop_item_id>", methods=["POST"], endpoint="buy_item")
@login_required
def buy_item(shop_item_id):
    form = ShopForm()

    if not form.validate_on_submit():
        return redirect(url_for("shop.shop"))

    user = current_user
    qty = form.quantity.data

    shop_item = ShopItem.query.get_or_404(shop_item_id)
    item = shop_item.item

    cost = item.base_price * qty

    # Check stock
    if shop_item.quantity < qty:
        flash("Not enough stock in the shop.", "danger")
        return redirect(url_for("shop.shop"))

    # Check coins
    if user.current_coins < cost:
        flash("Not enough coins.", "danger")
        return redirect(url_for("shop.shop"))

    # Deduct coins
    user.current_coins -= cost

    # Reduce shop stock
    shop_item.quantity -= qty

    # --- NEW INVENTORY SYSTEM ---
    # Get or create the user's inventory (one per user)
    inventory = user.inventory
    if inventory is None:
        inventory = Inventory(user_id=user.id)
        db.session.add(inventory)
        db.session.flush()  # ensures inventory.id exists

    # Find or create the InventoryItem entry
    inv_item = InventoryItem.query.filter_by(
        inventory_id=inventory.id,
        item_id=item.id
    ).first()

    if not inv_item:
        inv_item = InventoryItem(
            inventory_id=inventory.id,
            item_id=item.id,
            quantity=0
        )
        db.session.add(inv_item)

    # Add quantity
    inv_item.quantity += qty

    db.session.commit()

    flash(f"{qty} {item.name} added to inventory.", "success")
    return redirect(url_for("shop.shop"))


