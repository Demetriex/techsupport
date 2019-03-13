import os
from flask import url_for, current_app
from werkzeug.utils import secure_filename
from datetime import datetime


def save_file(file_upload, request_number):
    filename = file_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = request_number + '.' + ext_type
    # from flask
    secured = secure_filename(storage_filename)
    filepath = os.path.join(current_app.root_path, 'files\Attachment', secured)
    file_upload.save(filepath)
    # return secured file name
    return secured


def new_file_name(email, RequestNumber):
    return f"{email}-{RequestNumber:05}"
