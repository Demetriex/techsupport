# create error handler
from flask import render_template, Blueprint

error_handler = Blueprint('error_handler', __name__)


@error_handler.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/error_404.html'), 404


@error_handler.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/error_403.html'), 403


@error_handler.app_errorhandler(500)
def error_500(error):
    return render_template('error_pages/error_500.html'), 500
