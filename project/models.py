# create database models
# import from SQL ALCHEMY
from project import db
from datetime import datetime
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    active = db.Column(db.Boolean(), default=False)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    password = db.Column(db.String(255))
    department = db.Column(db.String(64))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    requests = db.relationship('RequestTicket', backref='owner')


class RequestTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String())
    description = db.Column(db.String())
    department = db.Column(db.String())
    local_number = db.Column(db.String())
    location = db.Column(db.String())
    other_contact = db.Column(db.String())
    date_requested = db.Column(db.DateTime())
    file_attached = db.Column(db.String())
    status = db.Column(db.String())
    assigned_to = db.Column(db.String())
    assigned_name = db.Column(db.String())
    recommended_by = db.Column(db.String())
    recommendation = db.Column(db.String())
    action_taken = db.Column(db.String())
    track_code = db.Column(db.String(),unique=True)

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('request_ticket.id'), nullable=False)
    technician = db.Column(db.String())
    rating = db.Column(db.String())
    feedback = db.Column(db.String())
