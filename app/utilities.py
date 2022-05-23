import base64
import time
import os
from werkzeug.utils import secure_filename
from flask import render_template
from sqlalchemy import select, or_
from app.models import User, db


def allowed_file(file: str, app):
    return '.' in file and os.path.splitext(
        file)[1][1:].lower() in app.config['ALLOWED_FILE_EXTENSIONS']


def make_filename(filename=None):
    if filename:
        name, ext = os.path.splitext(filename)
    else:
        name = ''
        ext = '.png'
    name = '{}{}'.format(name, round(time.time()))
    return name + ext


def upload_file(*, file, dest: str, app):
    '''
    uploads the file to a given destination
    '''
    dest = dest.upper()
    if file is not None and file.filename != '' and \
    allowed_file(file.filename, app):
        filename = secure_filename(file.filename)
        filename = make_filename(filename)
        file.save(os.path.join(app.config[dest], filename))
        return filename
    return False


def delete_file(*, filename):
    os.remove(os.path.join('app', 'static', filename))


def email_or_phone_exists(*, email: str, phone: str, session):
    user = session.execute(
        select(User).where(or_(User.phone == phone,
                               User.email == email))).all()
    if user:
        return True
    return False


def upload_from_string(*, file_string, app, dest):
    '''
    upload a file from a bytes string to the server
    '''
    filename = make_filename()
    file = open(os.path.join(app.config[dest.upper()], filename), 'wb')
    file.write(base64.b64decode(file_string))
    file.close()
    return  os.path.join(dest,filename)