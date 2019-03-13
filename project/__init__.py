# project/__init__.py

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile(filename='config.py')

db = SQLAlchemy(app)

#####################flask-Migrate##########################
from flask_migrate import Migrate
migrate = Migrate(app, db)

#####################flask - security#######################
from flask_security import Security, SQLAlchemyUserDatastore, user_registered
from project.models import User, Role, RequestTicket, Departments,Feedback
from project.customforms import ExtendedLoginForm, ExtendedRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm,
                    register_form=ExtendedRegisterForm)


@user_registered.connect_via(app)
def on_user_registered(sender, user, confirm_token):
    user.active = False
    db.session.commit()

####################flask-admin#############################


from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from project.models import User, Role
from flask_security import current_user, utils
from wtforms import PasswordField
from flask_admin.menu import MenuLink


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.has_role('super-admin'):
            return self.render('admin.html')
    def is_accessible(self):
        return current_user.has_role('super-admin')


admin = Admin(app, name='CEUTECHSUPPORT', template_mode='bootstrap3', index_view=MyHomeView())


class ModelViewNoPass(ModelView):
    def is_accessible(self):
        return current_user.has_role('super-admin')


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.has_role('super-admin')
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)

    def scaffold_form(self):
        form_class = super(MyModelView, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)


admin.add_view(MyModelView(User, db.session))
admin.add_view(ModelViewNoPass(Role, db.session))
admin.add_view(ModelViewNoPass(RequestTicket, db.session))
admin.add_view(ModelViewNoPass(Departments, db.session))
admin.add_view(ModelViewNoPass(Feedback, db.session))
admin.add_link(MenuLink(name='Return to Main Page', category='', url='/'))

######################register blueprint#####################
from project.common.views import common
from project.error_handler.handlers import error_handler
from project.admin.views import administrator
from project.request.views import requests
from project.manage_user.views import manage
from project.search.search import search

app.register_blueprint(common)
app.register_blueprint(error_handler)
app.register_blueprint(administrator)
app.register_blueprint(requests)
app.register_blueprint(manage)
app.register_blueprint(search)
