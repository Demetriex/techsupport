from flask import Flask, request, url_for, redirect, flash, Blueprint, render_template, request
from project import user_datastore, db
from flask_security import roles_required, login_required
from project.models import User, Departments
from project.admin.forms import AddDepartment

administrator = Blueprint('administrator', __name__)


@administrator.route('/Activate/<email>', methods=['POST', 'GET'])
@roles_required('admin')
def activate_user(email):
    user = user_datastore.get_user(email)
    user_datastore.activate_user(user)
    db.session.commit()
    flash(f'{email} has been activated')
    return redirect(url_for('common.user_page', email=user.email))


#@administrator.route('/AddDepartment', methods=['POST', 'GET'])
#@roles_required('admin')
def add_department():
    form = AddDepartment()
    items = Departments.query.all()
    if form.validate_on_submit():
        depa = Departments(name=form.department.data)
        db.session.add(depa)
        db.session.commit()
        flash('Successfully added new Department')
        return redirect(url_for('administrator.add_department'))
    elif request.method == 'GET':
        items = Departments.query.all()
        form.department.data = None

    return render_template('admin/add_department.html', form=form, items=items)


#@administrator.route('/DeleteDepartment/<int:id>', methods=['POST'])
#@roles_required('admin')
def delete_department(id):
    department = db.session.query(Departments).filter_by(id=id).one()
    db.session.delete(department)
    db.session.commit()
    flash(f'Successfully deleted the {department.name} (department)')
    return redirect(url_for('administrator.add_department'))
