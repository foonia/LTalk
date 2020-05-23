# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

from .config import config_by_name


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    app.register_blueprint(general_bp)
    socketio.init_app(app)

    return app


from app.general.cotroller.main_controller import general_bp
