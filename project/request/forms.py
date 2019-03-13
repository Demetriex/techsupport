from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from project.models import User, Role
from project import db, user_datastore


class RequestTicketForm(FlaskForm):
    title = SelectField('Problem', validators=[DataRequired()],
                        choices=[('Computer Software Problem', 'Computer Software Problem'),
                                 ('No Internet Connection', 'No Internet Connection'),
                                 ('Operating System Problem', 'Operating System Problem'),
                                 ('Defective CPU', 'Defective CPU'),
                                 ('Defective Monitor', 'Defective Monitor'),
                                 ('Defective Keyboard', 'Defective Keyboard'),
                                 ('Defective Mouse', 'Defective Mouse'),
                                 ('Others', 'Others')
                                 ])
    description = TextAreaField('Problem Description/Observations', validators=[DataRequired(255)])
    location = StringField('Location', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    local_number = IntegerField('Local Number', validators=[DataRequired('Enter Valid Number')])
    other_contact = StringField('Other Contact Details', validators=[DataRequired()])
    file = FileField('Optional Attachment', validators=[FileAllowed(['docx', 'pdf', 'jpg'])])
    submit = SubmitField('Submit Request')


class RecommendationForm(FlaskForm):
    recommendation = TextAreaField('Recommendation(For Repair,For Replacement,Others)', validators=[
                                   DataRequired('Please type A Recommendation')])
    submit = SubmitField('Submit Recommendation')
