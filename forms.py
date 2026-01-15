from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
from wtforms import StringField
from wtforms.validators import Optional, URL


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[Optional(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")



class TodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField("Category",choices=[
        ("main", "Main Quest"),
        ("side", "Side Quest")
        ],
        validators=[DataRequired()])
    submit = SubmitField("Submit")
