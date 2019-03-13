from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RoleForm(FlaskForm):
    role = SelectField('Role', choices=[('tech-support', 'Tech-Support'), ('admin', 'Admin')])
    submit = SubmitField('Add Role')

class UpdatePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),EqualTo(
        'pass_confirm', message='Passwords Must Match!'), Length(6)])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired(),Length(6)])
    submit = SubmitField('Update Password')
