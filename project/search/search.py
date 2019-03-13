from flask import Blueprint, render_template,request,url_for,abort,redirect
from flask_security import login_required
from project.models import RequestTicket,User
from project import db
from flask_security import current_user

search = Blueprint('search', __name__)


@search.route('/search/track/', methods=['GET','POST'])
@login_required
def track():
    report = None
    owner = None
    if request.method == 'POST':
        if request.form['searchfield'] != None:
            report = db.session.query(RequestTicket).filter(RequestTicket.track_code==request.form['searchfield']).first()
        if report != None:
            owner = db.session.query(User).filter(User.id==report.owner_id).first()
            if owner.id == current_user.id or current_user.has_role('super-admin') or current_user.has_role('admin') or current_user.has_role('tech-support'):
                pass
            else:
                abort(403)
    msg = None
    if request.method == 'GET':
        msg = "hello"

    return render_template('/search/track.html', report=report,owner=owner,msg=msg)
