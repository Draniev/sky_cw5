from flask import Flask

from .config import Config
from .setup.db import db
from .views import main_blueprint


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    return app


def register_extensions(app: Flask):
    db.init_app(app)
    app.register_blueprint(main_blueprint)


def page_index():
    pass
