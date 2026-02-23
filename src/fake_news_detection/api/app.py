import os
import secrets

from flask import Flask

from ..config import STATIC_DIR
from ..database.repository import init_db


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(STATIC_DIR))
    secret_key = os.getenv("FLASK_SECRET_KEY")
    if not secret_key:
        app.logger.warning(
            "FLASK_SECRET_KEY is not set; using a temporary secret key. Sessions will be invalidated on restart."
        )
        secret_key = secrets.token_hex(32)
    app.secret_key = secret_key

    from .routes import api_blueprint

    app.register_blueprint(api_blueprint)
    init_db()
    return app
