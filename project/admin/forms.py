from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddDepartment(FlaskForm):
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Add Department')
