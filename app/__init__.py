import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('defaultConfig.py')

    os.makedirs(app.config['UPLOADS'], exist_ok=True)
    os.makedirs(app.config['DOCUMENTS'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_pyfile('defaultConfig.py')

    # bind extensions to the app
    from app.models import db, init_app
    init_app(app)
    from flask_migrate import Migrate
    db.init_app(app)
    Migrate(app, db)

    # register blueprints
    from app.auth import auth
    from app.main import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app