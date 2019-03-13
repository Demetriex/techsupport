# run app here $python app.py
#initialized in project/__init__.py
from flask import render_template
from project import app, db, user_datastore
from flask_security import login_required
from flask_security import utils


@app.before_first_request
def before_first_request():
    # Create any database tables that don't exist yet.
    db.create_all()

    user_datastore.find_or_create_role(name='super-admin', description='Super-Admin')
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='tech-support', description='Technician')

    if not user_datastore.get_user('admin@admin.com'):
        user_datastore.create_user(email='admin@admin.com', password='mysecretpassword',firstname='Lesser',lastname='Ajax',active=True)
    db.session.commit()
    if not user_datastore.get_user('super@admin.com'):
        user_datastore.create_user(email='super@admin.com', password=utils.encrypt_password('superpassword'),firstname='Greater',lastname='Ajax',active=True)
    db.session.commit()

    user_datastore.add_role_to_user('admin@admin.com', 'XXXXX')
    db.session.commit()
    user_datastore.add_role_to_user('super@admin.com', 'XXXXX')
    db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    #set debub=True if testing
    app.run()
