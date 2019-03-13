from flask import Blueprint, render_template, flash, request,redirect,url_for
from flask_wtf import FlaskForm
from flask_security import roles_accepted
from project import user_datastore
from flask_security import utils, current_user
from project import db
from project.models import User, Role
from project.manage_user.forms import CreateUserForm, UpdatePassword
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

manage = Blueprint('manage', __name__)


@manage.route('/create_account', methods=['GET', 'POST'])
@roles_accepted('admin', 'super-admin')
def create_account():
    form = CreateUserForm()

    if form.validate_on_submit():
        if not user_datastore.get_user(form.email.data):
            user_datastore.create_user(email=form.email.data,
                                       password=utils.encrypt_password('12345CEU'),
                                       firstname=form.firstname.data,
                                       lastname=form.lastname.data,
                                       active=True)

            db.session.commit()
            if form.role.data != 'End-User':
                user_datastore.add_role_to_user(form.email.data, form.role.data)
                db.session.commit()
            flash('Account Created')
        else:
            flash('Email is already registered')
    return render_template('manage_user/create_account.html', form=form)


@manage.route('/manage/admin')
@roles_accepted('super-admin')
def admin_account():
    user_active = db.session.query(User).filter_by(
        active=True).filter(User.roles.any(Role.name == 'admin')).all()
    user_inactive = db.session.query(User).filter_by(
        active=False).filter(User.roles.any(Role.name == 'admin')).all()
    return render_template('manage_user/admin.html', user_active=user_active, user_inactive=user_inactive)


@manage.route('/manage/technician')
@roles_accepted('admin', 'super-admin')
def technician_account():
    user_active = db.session.query(User).filter_by(
        active=True).filter(User.roles.any(Role.name == 'tech-support')).all()
    user_inactive = db.session.query(User).filter_by(
        active=False).filter(User.roles.any(Role.name == 'tech-support')).all()
    return render_template('manage_user/technician.html', user_active=user_active, user_inactive=user_inactive)


@manage.route('/manage/end_user')
@roles_accepted('admin', 'super-admin')
def end_user_account():
    user_active = db.session.query(User).filter_by(active=True).filter(User.roles == None).all()
    user_inactive = db.session.query(User).filter_by(active=False).filter(User.roles == None).all()
    return render_template('manage_user/end_user.html', user_active=user_active, user_inactive=user_inactive)


@manage.route('/manage/update/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'super-admin')
def update_account(id):
    user = db.session.query(User).filter(User.id == id).first()
    class EditUserForm(FlaskForm):
        if current_user.has_role('super-admin') or current_user.id == user.id:
            choice = [('End-User', 'End-User'), ('tech-support',
                                                 'Tech-Support'), ('admin', 'Admin')]
        else:
            choice = [('End-User', 'End-User'), ('tech-support', 'Tech-Support')]
        email = StringField('Email', validators=[DataRequired(), Email()])
        firstname = StringField('First Name', validators=[DataRequired()])
        lastname = StringField('Last Name', validators=[DataRequired()])
        role = SelectField('Role',
                           choices=choice)
        active = BooleanField('Activate/Deactivate')
        submit = SubmitField('Update User')

    form = EditUserForm()
    passw = UpdatePassword()
    if passw.validate_on_submit():
        user.password = utils.encrypt_password(passw.password.data)
        db.session.commit()
        flash('Successfully updated the user password')
        return redirect(url_for('manage.update_account',id=user.id))

    if form.validate_on_submit():
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.active = form.active.data
        db.session.commit()
        for role in user.roles:
            if form.role.data == 'admin':
                if role == 'tech-support':
                    user_datastore.remove_role_from_user(user.email,'tech-support')
                    db.session.commit()
            if form.role.data == 'tech-support':
                if role == 'admin':
                    user_datastore.remove_role_from_user(user.email,'admin')
                    db.session.commit()
            if  form.role.data == 'End-User':
                if role == 'admin':
                    user_datastore.remove_role_from_user(user.email,'admin')
                    db.session.commit()
                elif role == 'tech-support':
                    user_datastore.remove_role_from_user(user.email,'tech-support')
                    db.session.commit()

        if form.role.data != 'End-User':
            user_datastore.add_role_to_user(form.email.data, form.role.data)
            db.session.commit()
        flash('Successfully updated user')
        return redirect(url_for('manage.update_account',id=user.id))

    if request.method == 'GET':
        form.email.data = user.email
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.active.data = user.active
        for role in user.roles:
            if role == 'admin':
                form.role.data = 'admin'
            elif role == 'tech-support':
                form.role.data = 'tech-support'
            else:
                form.role.data = 'End-User'


    return render_template('manage_user/update_account.html', form=form, passw=passw,id=id)
