from flask_wtf import FlaskForm
from flask_security.forms import RegisterForm, LoginForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_wtf.recaptcha import RecaptchaField


class ExtendedLoginForm(LoginForm):
    email = StringField('Email', [DataRequired(message='Email is required '), Email(
        message='Invalid email address')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', [DataRequired(message='password is required')], render_kw={
                             "placeholder": "Password"})
    recaptcha = RecaptchaField()
    remember = BooleanField('Remember Me')


class ExtendedRegisterForm(RegisterForm):
    firstname = StringField('First Name', [DataRequired()])
    lastname = StringField('Last Name', [DataRequired()])
    recaptcha = RecaptchaField()
