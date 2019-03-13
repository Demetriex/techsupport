import os
from flask import Blueprint, request, url_for, render_template, flash, redirect, send_from_directory, current_app, abort
from flask_security import login_required, current_user, roles_accepted
from project import db, user_datastore, app
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from sqlalchemy import desc
from project.request.action import for_action
from wtforms.validators import DataRequired
from project.request.assign import auto_technician
from project.request.tracking_code_generator import generate_code
from project.request.forms import RequestTicketForm, RecommendationForm
from project.request.file_handler import save_file, new_file_name
from project.models import RequestTicket, User, Feedback, Role


requests = Blueprint('requests', __name__)

################################################################################


@requests.route('/uploads/<path:filename>')
def file_download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)

################################################################################


@requests.route('/request/<ownerid>/<ticketno>/', methods=['GET', 'POST'])
@login_required
def tickets_view(ownerid, ticketno):
    tech = db.session.query(User).filter(User.roles.any(Role.name == 'tech-support')).all()
    request = RequestTicket.query.filter_by(id=ticketno, owner_id=ownerid).first_or_404()
    list = []
    for user in tech:
        if 'tech-support' in user.roles:
            choice = (user.email, f"{user.firstname} {user.lastname}")
            list.append(choice)

    class AssignForm(FlaskForm):
        technician = SelectField('Technician', validators=[DataRequired()], choices=list)
        submit = SubmitField('Assign')

    class ActionForm(FlaskForm):
        action = for_action(request.title)
        if action == 'repair_only':
            choice = [('Repaired', 'Repaired'),
                     ]
        else:
            choice = [('Repaired', 'Repaired'),
                     ('Replaced', 'Replaced'),
                     ]

        action = SelectField('Action Taken', validators=[DataRequired('Please type the Action Taken')],
                             choices=choice)
        submit = SubmitField('Submit Action')

    form = AssignForm()
    rec_form = RecommendationForm()
    act_form = ActionForm()
    owner = user_datastore.get_user(ownerid)
    recommended_user = user_datastore.get_user(request.recommended_by)
    assign_user = user_datastore.get_user(request.assigned_to)
    feedback = Feedback.query.filter_by(ticket_id=ticketno).first()

    if request.status == 'Pending' and current_user.email == request.assigned_to:
        request.status = 'On-Going'
        db.session.commit()

    if rec_form.validate_on_submit():
        request.recommendation = rec_form.recommendation.data
        request.recommended_by = current_user.email
        db.session.commit()
        flash("You added recomendation to the problem")
        return redirect(url_for('requests.tickets_view', ownerid=request.owner_id, ticketno=request.id))

    if act_form.validate_on_submit():
        request.action_taken = act_form.action.data
        request.status = act_form.action.data
        db.session.commit()
        flash("You added the actions taken")
        return redirect(url_for('requests.tickets_view', ownerid=request.owner_id, ticketno=request.id))

    if form.validate_on_submit():
        if form.technician.data:
            request.status = 'Pending'
            request.assigned_to = form.technician.data
            user = user_datastore.get_user(form.technician.data)
            request.assigned_name = f"{user.firstname} {user.lastname}"
            db.session.commit()
            flash("Successfully assigned a technician")
            return redirect(url_for('requests.tickets_view', ownerid=request.owner_id, ticketno=request.id))

    if current_user.has_role('super-admin') or current_user.has_role('admin') or current_user.has_role('tech-support') or owner.id == current_user.id:
        return render_template('/request/view_request.html',
                               request=request,
                               owner=owner,
                               form=form,
                               rec_form=rec_form,
                               act_form=act_form,
                               recommended_user=recommended_user,
                               assign_user=assign_user,
                               feedback=feedback
                               )
    else:
        abort(403)

################################################################################


@requests.route('/request', methods=['GET', 'POST'])
@login_required
def request_ticket():
    if current_user.has_role('tech-support') or current_user.has_role('admin'):
        flash('You can not create a ticket')
        return redirect(url_for('index'))
    else:
        pass
    form = RequestTicketForm()
    myfile = None
    if form.validate_on_submit():
        if form.file.data:
            number = db.session.query(User).join(User.requests).filter(
                RequestTicket.owner_id == current_user.id).count()

            myfile = save_file(form.file.data, new_file_name(current_user.email, number))
        technician = auto_technician()  # from assign py
        # get technician name
        name = User.query.filter_by(email=technician).first()
        tech_name = f"{name.firstname} {name.lastname}"
        code = generate_code()
        NewTicket = RequestTicket(owner_id=current_user.id,
                                  title=form.title.data,
                                  description=form.description.data,
                                  department=form.department.data,
                                  local_number=form.local_number.data,
                                  location=form.location.data,
                                  other_contact=form.other_contact.data,
                                  date_requested=datetime.utcnow(),
                                  file_attached=myfile,
                                  status='Pending',
                                  assigned_to=technician,
                                  assigned_name=tech_name,
                                  track_code=code
                                  )
        db.session.add(NewTicket)
        db.session.commit()
        flash('Request Submitted')
        return redirect(url_for('requests.code',code=code))

    return render_template('/request/request.html', form=form)

################################################################################


@requests.route('/request/pending')
@roles_accepted('admin', 'super-admin')
def pending_tickets():
    tickets = db.session.query(RequestTicket, User)\
        .outerjoin(User, RequestTicket.owner_id == User.id)\
        .order_by(desc(RequestTicket.date_requested))\
        .filter(RequestTicket.status == 'Pending')
    return render_template('/request/requests_pending.html', tickets=tickets)

################################################################################


@requests.route('/request/all')
@roles_accepted('admin', 'super-admin', 'tech-support')
def all_tickets():
    tickets = db.session.query(RequestTicket, User)\
        .outerjoin(User, RequestTicket.owner_id == User.id)\
        .order_by(desc(RequestTicket.date_requested))
    #name = db.session.query(User).filter_by(User.email==tickets)
    return render_template('/request/requests_all.html', tickets=tickets)

################################################################################


@requests.route("/request/assigned")
@login_required
def assigned_tickets():
    tickets = db.session.query(RequestTicket, User)\
        .outerjoin(User, RequestTicket.owner_id == User.id)\
        .filter(RequestTicket.assigned_to == current_user.email)

    return render_template('/request/requests_assigned.html', tickets=tickets)

################################################################################


@requests.route("/request/feedback/<requestid>/<ownerid>/<technician>", methods=['POST'])
def feedback(ticketid, ownerid, technician):
    user = User.query.filter_by(id=ownerid).first_or_404()
    if user.id == current_user.id:
        pass
    else:
        abort(404)
    textfb = request.form['text-feedback']
    rate = request.form['rating']
    feed = Feedback(ticket_id=ticketid,
                    technician=technician,
                    rating=rate,
                    feedback=textfb
                    )
    db.session.add(feed)
    db.session.commit()
    flash("Thanks for submitting your feedback")
    return redirect(url_for('requests.tickets_view', requestid=requestid, ownerid=ownerid))


################################################################################


@requests.route("/request/code/<code>")
@login_required
def code(code):
    request = db.session.query(RequestTicket).filter(RequestTicket.track_code==code).first_or_404()
    code = request.track_code
    return render_template('/request/code.html',code=code)
