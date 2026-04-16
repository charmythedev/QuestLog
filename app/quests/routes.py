# app/quests/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import Todo, CompletedQuest
from app.leveling import (
    level_up,
    gain_xp,
    gain_coins,
    productive_xp,
    multiplier,
    xp_value,
    coin_value,
)

from app.forms import TodoForm   # ← FIXED: must come from app.forms
from . import quests_bp



@quests_bp.route("/QuestLog", methods=["GET", "POST"], endpoint="quest_log")
@login_required
def quest_log():
    user = current_user
    form = TodoForm()

    # Create new quest
    if form.validate_on_submit():
        new_todo = Todo(
            title=form.title.data,
            category=form.category.data,
            completed=False,
            user_id=current_user.id  # ← FIXED
        )

        new_todo.xp = xp_value(new_todo, current_user)
        new_todo.coins = coin_value(new_todo)

        db.session.add(new_todo)
        db.session.commit()

        flash("New Quest Added!", "success")
        return redirect(url_for("quests.quest_log"))   # ← FIXED
    # Sorting
    sort = request.args.get("sort")
    category = request.args.get("category")

    query = Todo.query.filter_by(user_id=user.id)

    if category:
        query = query.filter_by(category=category)

    if sort == "date":
        query = query.order_by(Todo.date.desc())
    elif sort == "title":
        query = query.order_by(Todo.title.asc())
    elif sort == "xp":
        query = query.order_by(Todo.xp.desc())

    page = request.args.get("page", 1, type=int)
    todos = query.paginate(page=page, per_page=9)

    return render_template(
        "quest_log.html",
        user=user,
        todos=todos,
        form=form
    )

@quests_bp.route("/remove/<int:todo_id>", methods=["POST"], endpoint="remove")
@login_required
def remove(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    # Make sure the user owns this quest
    if todo.user_id != current_user.id:
        flash("You cannot delete someone else's quest.", "danger")
        return redirect(url_for("quests.quest_log"))

    db.session.delete(todo)
    db.session.commit()

    flash("Quest removed!", "success")
    return redirect(url_for("quests.quest_log"))

@quests_bp.route("/turn-in/<int:todo_id>", methods=["POST"], endpoint="turn_in")
@login_required
def turn_in(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    # Ensure user owns the quest
    if todo.user_id != current_user.id:
        flash("You cannot turn in someone else's quest.", "danger")
        return redirect(url_for("quests.quest_log"))

    # Mark completed so gain_xp() logic works
    todo.completed = True

    # Award XP + coins BEFORE deleting the quest
    gain_xp(current_user, todo.xp)      # XP now works
    gain_coins(current_user, todo.coins)  # Coins now work
    level_up(current_user)

    # Move quest to CompletedQuest
    completed = CompletedQuest(
        user_id=current_user.id,
        title=todo.title,
        xp=todo.xp,
        date_completed=datetime.utcnow()
    )

    db.session.add(completed)
    db.session.delete(todo)
    db.session.commit()

    flash("Quest turned in!", "success")
    flash(f"+{todo.coins} coins, and +{todo.xp} XP gained!", "success")
    return redirect(url_for("quests.quest_log"))
