# app/auth/routes.py

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User
from app.email_utils import send_reset_email, verify_reset_token
from app.forms import RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm

from . import auth_bp


# -------------------------
# REGISTER
# -------------------------
@auth_bp.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        ).scalar_one_or_none()

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for('auth.login'))

        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8
        )

        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=hashed_password,

        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return redirect(url_for('main.index'))

    return render_template("register.html", form=form)


# -------------------------
# LOGIN
# -------------------------
@auth_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Welcome Back!', 'success')
            return redirect(url_for('quests.quest_log'))
        else:
            flash("(╯°□°）╯︵ ┻━┻ Login failed!", "danger")

    return render_template("login.html", form=form)


# -------------------------
# RESET PASSWORD REQUEST
# -------------------------
@auth_bp.route('/reset-password', methods=['GET', 'POST'], endpoint='reset_password_request')
def reset_password_request():
    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        ).scalar_one_or_none()

        if user:
            send_reset_email(user)

        flash("If that email exists, reset instructions have been sent.")
        return redirect(url_for('login'))

    return render_template('reset_password_request.html', form=form)


# -------------------------
# RESET PASSWORD (TOKEN)
# -------------------------
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'], endpoint='reset_password')
def reset_password(token):
    email = verify_reset_token(token)

    if not email:
        flash("Invalid or expired token.")
        return redirect(url_for('reset_password_request'))

    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        flash("User not found.")
        return redirect(url_for('reset_password_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8
        )
        user.password = hashed
        db.session.commit()
        flash("Password updated successfully.")
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


# -------------------------
# LOGOUT
# -------------------------
@auth_bp.route('/logout', endpoint='logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for('main.index'))
