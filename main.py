from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import os

#### FLASK CONFIG ######
date = datetime.now().year
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', "sqlite:///local.db")

#### CREATE DATABASE ####
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    date: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    coins: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    completed: Mapped[bool] = mapped_column(default=False)
    xp_given: Mapped[bool] = mapped_column(default=False)
    coins_received : Mapped[bool] = mapped_column(default=False)
    user = relationship("User", back_populates="todos")

#new table altered in psql

class CompletedQuest(db.Model):
    __tablename__ = "completed_quests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)
    date_completed: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="completed_quests")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    level: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    current_xp: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    next_level_xp = mapped_column(Integer, default=100)
    current_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    todos = relationship("Todo", back_populates="user", cascade="all, delete")
    completed_quests = relationship("CompletedQuest", back_populates="user", cascade="all, delete")
    quests_completed = mapped_column(Integer, default=0)
    last_bonus_date = db.Column(db.Date, nullable=True)



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

def gain_xp(user):
    current_xp = user.current_xp
    for task in user.todos:
        if task.completed and not task.xp_given:
            user.quests_completed += 1
            current_xp += task.xp
            task.xp_given = True
    user.current_xp = current_xp
    db.session.commit()
    return user.current_xp

def gain_coins(user):
    current_coins = user.current_coins
    for task in user.todos:
        if task.completed and not task.coins_received:

            current_coins += task.coins
            task.coins_received = True
    user.current_coins = current_coins
    db.session.commit()
    return user.current_coins

def productive_xp(user):
    streak = 5
    today = datetime.today().date()


    completed_today = sum(
        1 for quest in user.completed_quests
        if quest.date_completed.date() == today
    )

    if completed_today >= streak and user.last_bonus_date != today:
        user.last_bonus_date = today
        user.current_xp += 50
        db.session.commit()
        return True

    return False

def xp_value(todo):
    xp_map = {
        "main": 25,
        "work": 15,
        "errand": 10,
        "daily": 10,
        "side": 20,
        "personal": 25,
        "other": 10
    }

    return xp_map.get(todo.category, 5)

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
    10: "Grand Archmage of Getting Stuff Done"
}

#### Avatar ####
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro')

### BUILD FLASK ROUTES ###
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar_one_or_none()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for('login'))
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    #todo change this to redirect(url_for('profile') or something later
    return render_template("register.html", form=form, date=date)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
        if user and check_password_hash(user.password, password):

            login_user(user)
            flash('Welcome Back!', 'success')

            return redirect(url_for('index'))
        else:
            flash("(╯°□°）╯︵ ┻━┻ Login failed!", "danger")

    return render_template("login.html", form=form, date=date)


@app.route("/")
def index():
    return render_template("index.html", date=date)

@app.route("/profile")
@login_required
def profile():
    user = current_user
    todos = user.todos
    user.title = LEVEL_TITLES.get(user.level, "Quester")

    page = request.args.get('page', 1, type=int)
    query = CompletedQuest.query.filter_by(user_id=user.id)
    completed = query.paginate(page=page, per_page=15)
    return render_template("profile.html", user=user, todos=todos, date=date, completed=completed)

@app.route("/QuestLog", methods=['GET', 'POST'])
@login_required
def quest_log():
    user = current_user

    #create new quest form:

    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(title=form.title.data,
                        category=form.category.data,
                        completed=False,
                        user=current_user)
        new_todo.xp = xp_value(new_todo)
        new_todo.coins = coin_value(new_todo)
        db.session.add(new_todo)
        db.session.commit()
        flash("New Quest Added!", "success")
        return redirect(url_for('quest_log'))

    # Sorting and pagination logic

    page = request.args.get('page', 1, type=int)
    query = Todo.query.filter_by(user_id=user.id)

    sort = request.args.get('sort')
    category = request.args.get("category")

    if category:
        query = query.filter_by(category=category)

    if sort == "date":
        query = query.order_by(Todo.date.desc())
    elif sort == "title":
        query = query.order_by(Todo.title.asc())
    elif sort == "xp":
        query = query.order_by(Todo.xp.desc())
    else:
        query = query.order_by(Todo.date.desc())

    todos = query.paginate(page=page, per_page=6)

    return render_template("quest_log.html", user=user, todos=todos, date=date, form=form)
@app.route("/turn-in/<int:todo_id>", methods=["POST"])
@login_required
def turn_in(todo_id):
    todo = db.session.get(Todo, todo_id)
    todo.completed = True
    bonus = productive_xp(current_user)

    xp_added = gain_xp(current_user)
    gain_coins(current_user)
    leveled = level_up(current_user)
    if leveled:
        flash('LEVEL UP!', 'success')
    completed = CompletedQuest(
        user_id=current_user.id,
        title=todo.title,
        xp=todo.xp
    )
    db.session.add(completed)
    db.session.delete(todo)
    if xp_added:
        flash(f'{todo.xp} xp gained!', 'success')
    if bonus:
        flash('5 quests in 1 day! BONUS XP +50', 'success')
    if todo.coins_received:
        flash(f'+ {todo.coins} coins gained!', 'success')
    db.session.commit()

    return redirect(url_for("quest_log"))

@app.route("/remove/<int:todo_id>", methods=["POST"])
@login_required
def remove(todo_id):
        todo = db.session.get(Todo, todo_id)
        todo.completed = False
        if not todo:
            flash("Quest does not exist!", "danger")
            return redirect(url_for('quest_log'))

        if todo.user != current_user:
            flash("You do not have permission to do that!", "danger")
            return redirect(url_for('quest_log'))

        db.session.delete(todo)
        db.session.commit()

        return redirect(url_for("quest_log"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=False, port = 5002)


# todo create dict to add titles to levels

