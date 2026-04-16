# app/main/routes.py

from flask import render_template, request
from flask_login import login_required, current_user

from app.models import CompletedQuest
from app.leveling import LEVEL_TITLES

from . import main_bp


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
        completed=completed
    )
