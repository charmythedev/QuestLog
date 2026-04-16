# app/email_utils.py

import os
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# -------------------------
# TOKEN GENERATION
# -------------------------

def _get_serializer():
    """Return a serializer using the app's SECRET_KEY."""
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def generate_reset_token(email):
    s = _get_serializer()
    return s.dumps(email, salt="password-reset-salt")


def verify_reset_token(token, expiration=3600):
    s = _get_serializer()
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=expiration)
    except Exception:
        return None
    return email


# -------------------------
# SEND RESET EMAIL
# -------------------------

def send_reset_email(user):
    token = generate_reset_token(user.email)

    # Use blueprint endpoint name
    reset_url = url_for("auth.reset_password", token=token, _external=True)

    sender_email = os.environ.get("GOOGLE_EMAIL")
    api_key = os.environ.get("QUEST_LOG_SG_API")

    message = Mail(
        from_email=sender_email,
        to_emails=user.email,
        subject="Reset Your Password",
        html_content=f"""
        <p>Hi {user.username},</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_url}">{reset_url}</a></p>
        <p>If you did not request this, you can safely ignore this email.</p>
        """,
    )

    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
    except Exception as e:
        print("SendGrid error:", e)
