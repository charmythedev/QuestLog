from datetime import datetime
from .extensions import db

###### levelling logic #####
def level_up(user):
    current_xp = user.current_xp
    xp_needed = user.next_level_xp

    if current_xp >= xp_needed:
        user.level += 1
        user.current_xp -= xp_needed
        user.next_level_xp = int(xp_needed + (xp_needed * 0.5))
        db.session.commit()
        return True

    return False


def gain_xp(user, amount=None):
    current_xp = user.current_xp

    mult = multiplier(user)
    for task in user.todos:
        if task.completed and not task.xp_given:
            amount = task.xp
            user.quests_completed += 1
            current_xp += task.xp * mult
            task.xp_given = True

    user.current_xp = current_xp
    db.session.commit()
    return user.current_xp


# todo return the xp gained not the total xp
def gain_coins(user, amount):
    current_coins = user.current_coins
    for task in user.todos:
        if task.completed and not task.coins_received:
            amount = task.coins

            current_coins += task.coins
            task.coins_received = True
    user.current_coins = current_coins
    db.session.commit()
    return user.current_coins
# todo return the coins gained not total coins


def multiplier(user):
    today = datetime.today().date()
    completed_today = sum(
        1 for quest in user.completed_quests
        if quest.date_completed.date() == today
    )
    if completed_today <= 9:
        mult = 1.0
    elif completed_today > 9:
        mult = 0.5
    else:
        mult = 1.0
    return mult


def productive_xp(user):
    streak = 5
    today = datetime.today().date()
    mult = multiplier(user)

    completed_today = sum(
        1 for quest in user.completed_quests
        if quest.date_completed.date() == today
    )

    if completed_today >= streak and user.last_bonus_date != today:
        user.last_bonus_date = today
        user.current_xp += user.next_level_xp//20 * mult
        db.session.commit()
        return True

    return False

def xp_value(todo, user):
    base = user.next_level_xp

    xp_map = {
        "main": base//10,
        "work": base//15,
        "errand": base//20,
        "daily": base//12,
        "side": base//10,
        "personal": base//10,
        "other": base//22
    }

    return int(xp_map.get(todo.category, 5))

def coin_value(todo):
    coin_map = {
        "main": 100,
        "work": 50,
        "errand": 20,
        "daily": 35,
        "side": 60,
        "personal": 150,
        "other": 10
    }

    return coin_map.get(todo.category, 5)

LEVEL_TITLES = {
    1: "Intrepid Taskling",
    2: "Aspiring Errand Knight",
    3: "Momentum Wrangler",
    4: "Certified Doer of Things",
    5: "Questline Navigator",
    6: "Productivity Pathfinder",
    7: "Master of Minor Miracles",
    8: "Relentless Progress Adept",
    9: "Champion of Checked Boxes",
    10: "Grand Archmage of Getting Stuff Done",
    11: "The Productive One",
    12: "Hero of Tasks",
}