from flask_security import login_required, current_user, roles_accepted
from flask import Blueprint, request, url_for, render_template, flash, redirect, abort
from project import db, user_datastore
from wtforms import SubmitField, SelectField, StringField, FileField
from flask_wtf import FlaskForm
from wtforms import ValidationError
from sqlalchemy import desc
from flask_security import utils
from project.common.forms import RoleForm,UpdatePassword
from project.common.picture_handler import add_profile_pic
from project.models import User, RequestTicket, Departments
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length

common = Blueprint('common', __name__)


@common.route("/edit/profile", methods=['GET', 'POST'])
@login_required
def profile():
    class UpdateUserForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        firstname = StringField('First Name', validators=[DataRequired()])
        lastname = StringField('First Name', validators=[DataRequired()])
        picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
        submit = SubmitField('Update')

        def check_email(self, field):
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Your email has been registered already!')

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            email = current_user.email
            pic = add_profile_pic(form.picture.data, email)
            current_user.profile_image = pic

        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('common.profile'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('/common/profile.html', profile_image=profile_image, form=form)


@common.route("/user/profile/<email>", methods=['GET', 'POST'])
@login_required
def user_page(email):
    form = RoleForm()
    account = User.query.filter_by(email=email).first_or_404()
    return render_template('/common/user_page.html', account=account, form=form)


@common.route("/user/reports")
def user_tickets():
    if current_user.has_role('admin') or current_user.has_role('super-admin') or current_user.has_role('tech-support'):
        abort(403)
    tickets = db.session.query(RequestTicket, User)\
        .outerjoin(User, RequestTicket.owner_id == User.id)\
        .order_by(desc(RequestTicket.date_requested))\
        .filter(RequestTicket.owner_id == current_user.id)\

    return render_template('/common/user_tickets.html', tickets=tickets)

@common.route("/user/update_password", methods=['GET','POST'])
def update_password():
    form = UpdatePassword()
    if form.validate_on_submit():
        current_user.password = utils.encrypt_password(form.password.data)
        db.session.commit()
        flash('You updated your passsword')
    return render_template('/common/update_password.html',form=form)
