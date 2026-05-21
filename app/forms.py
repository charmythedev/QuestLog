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

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Reset Password")



class TodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField("Category",choices=[
        ("main", "Main Quest"),
        ("side", "Side Quest"),
        ("work", "Work"),
        ("errand", "Errand"),
        ("daily", "Daily Quest"),
        ("personal", "Personal Quest"),
        ('other', 'Other')
        ],
        validators=[DataRequired()])
    submit = SubmitField("Submit")

class ShopForm(FlaskForm):
    quantity = SelectField(
        "Quantity",
        choices=[(1,"1"),(5,"5"),(10,"10"),(20, "20"),(100,'100')],
        coerce=int
    )
class AltShopForm(FlaskForm):
    quantity = SelectField("Quantity", coerce=int)

    def set_quantities(self, max_stock):
        base = [1, 5, 10 , 20, 50, 100, max_stock]
        unique = sorted(set(base))
        valid = [(q, str(q)) for q in unique if q <= max_stock]
        self.quantity.choices = valid

