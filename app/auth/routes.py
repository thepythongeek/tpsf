import datetime
from flask import request
from flask import current_app
from app.auth import auth
from app.models import User, db
import jwt


@auth.post('/register')
def register():
    print()
    user = User(**request.json)
    user.hash_password

    db.session.add(user)
    db.session.commit()

    token = jwt.encode(
        {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        }, current_app.config['SECRET_KEY'])

    return {"success": True, "body": {"token": token}}
