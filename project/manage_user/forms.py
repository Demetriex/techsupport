from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role',
                       choices=[('End-User', 'End-User'),
                                ('tech-support', 'Tech-Support'),
                                ('admin', 'Admin')],
                       validators=[DataRequired()])
    submit = SubmitField('Create User')

class UpdatePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'pass_confirm', message='Passwords Must Match!'), Length(6)])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired(), Length(6)])
    submit = SubmitField('Update Password')
