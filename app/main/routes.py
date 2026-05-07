# app/main/routes.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user


from app.models import CompletedQuest
from app.leveling import LEVEL_TITLES

from . import main_bp
from .. import db


# -------------------------
# HOME PAGE
# -------------------------
@main_bp.route("/", endpoint="index")
def index():
    # date is injected globally by context_processor
    return render_template("index.html")


# -------------------------
# PROFILE PAGE
# -------------------------
@main_bp.route("/profile", endpoint="profile")
@login_required
def profile():
    user = current_user
    todos = user.todos
    inventory = user.inventory

    # Update title based on level
    user.title = LEVEL_TITLES.get(user.level, "Quester")

    # Pagination for completed quests
    page = request.args.get("page", 1, type=int)
    query = CompletedQuest.query.filter_by(user_id=user.id)
    completed = query.paginate(page=page, per_page=15)


    return render_template(
        "profile.html",
        user=user,
        todos=todos,
        completed=completed,
        inventory=inventory
    )

@main_bp.route("/use/<int:item_id>", methods=["POST"], endpoint="use_item")
@login_required
def use_item(item_id):
    user = current_user
    inv = user.inventory

    # Find the item in the user's inventory
    inv_item = next((row for row in inv.items if row.item_id == item_id), None)

    if not inv_item or inv_item.quantity <= 0:
        flash("You don't have any of this item!", "danger")
        return redirect(url_for("main.profile"))

    item = inv_item.item

    if not item.consumable:
        flash("This item cannot be used.", "warning")
        return redirect(url_for("main.profile"))

    # Steam Potion logic
    if item.name == "Steam Potion":
        restored = item.effect_value
        user.steam = min(user.max_steam, user.steam + restored)

        inv_item.quantity -= 1
        if inv_item.quantity == 0:
            db.session.delete(inv_item)

        db.session.commit()

        flash(f"You used a Steam Potion! +{restored} steam restored.", "success")
        return redirect(url_for("main.profile"))

    flash("This item has no effect yet.", "info")
    return redirect(url_for("main.profile"))
