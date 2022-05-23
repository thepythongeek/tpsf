import jwt
from flask import Blueprint
from flask_login import LoginManager
from app.models import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

loginManager = LoginManager()


@loginManager.request_loader
def load_user(request):
    '''
    attempt to get the user from request headers or url argument
    '''
    try:
        token = request.headers.get('token')
        if token:
            userid = token['id']
            user = db.session.get(int(userid))
            return user
        return None
    except jwt.ExpiredSignatureError:
        print('|||||||||****')
        return None


from app.auth import routes