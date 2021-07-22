from flask import Flask
from flask_io import FlaskIO
from flask_sqlalchemy import SQLAlchemy


from config import get_env
from config.env import app_env


from .models import db

from .main import main as main_blueprint

io = FlaskIO()


def create_app(config_name):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = get_env('SECRET')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.env = config_name
    app.debug = get_env('DEBUG')
    app.config.from_object(app_env[config_name])
    app.config.from_pyfile('../config/env.py')


    db.init_app(app)
    io.init_app(app)

    app.register_blueprint(main_blueprint)


    return app