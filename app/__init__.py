import os
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .config import load_config
from .routes.web import web_bp
from .routes.api import api_bp

def create_app():
    app = Flask(__name__)
    cfg = load_config()
    app.config.update(cfg)
    app.secret_key = cfg.get("FLASK_SECRET", "dev-secret")

    CORS(app)

    # Blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


# def create_app():
#     app = Flask(__name__)
#     cfg = load_config()
#     app.config.update(cfg)
#     app.secret_key = cfg.get("FLASK_SECRET", "dev-secret")

#     CORS(app)

#     # Blueprints
#     app.register_blueprint(web_bp)
#     app.register_blueprint(api_bp, url_prefix="/api")

#     # ⭐ 把應用包在 /badminton-scoreboard 下
#     app.wsgi_app = DispatcherMiddleware(Flask("dummy"), {
#         "/badminton-scoreboard": app.wsgi_app
#     })

#     return app
