from sqlalchemy import Date, cast, and_
from datetime import date
from project import db
from project.models import User, RequestTicket, Role


def auto_technician():
    technician = db.session.query(User).filter(User.roles.any(Role.name == 'tech-support')).all()
    # query by technicians
    list = []
    count = None
    for tech in technician:
        count = db.session.query(RequestTicket)\
            .filter(RequestTicket.assigned_to == tech.email)\
            .count()
        user = (count, tech.email)
        list.append(user)
    # get lowest tuple pair
    lowest = min(list)
    return lowest[1]
