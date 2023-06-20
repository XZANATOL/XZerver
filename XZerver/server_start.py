from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from os import getenv

from XZerver import config

def create_server():
    """ Flask server factory """
    # Init server
    server = Flask(
        __name__,
        static_folder='static_global',
        static_url_path='/static_global/'
        )
    server.config["SECRET_KEY"] = getenv("server_secret_key")
    server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./db.sqlite"
    server.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    server.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=10)
    server.config["REMEMBER_COOKIE_REFRESH_EACH_REQUEST"] = True
    server.config['SESSION_PERMANENT'] = True

    # Extensions & Config init
    csrf = CSRFProtect()
    config.init()
    config.db.init_app(server)
    csrf.init_app(server)

    # from path.file import Blueprint as X
    from XZerver.server.home.routes import home as home_blueprint
    from XZerver.server.auth.routes import auth as auth_blueprint
    from XZerver.server.xdrive.xdrive import xdrive as xdrive_blueprint

    blueprints = [
        home_blueprint,
        auth_blueprint,
        xdrive_blueprint
    ]

    for blueprint in blueprints:
        server.register_blueprint(blueprint)

    # Init login manager
    from XZerver.server.auth.models import User as auth_User
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(server)

    # Admin panel config
    from XZerver.server.auth.forms import UserFrom as auth_UserFrom

    from XZerver.server.xdrive.forms import SharedFolderForm
    from XZerver.server.xdrive.models import SharedFolder
    from XZerver.server.xdrive.admin import xdrive_admin
    items = {
        "accounts": {"model": auth_User, "form": auth_UserFrom},
        "xdrive": {"model": SharedFolder, "form": SharedFolderForm, "admin": xdrive_admin}
    }

    for key, value in items.items():
        config.admn_pnl_mdl_reg.__setitem__(key, value)

    @login_manager.user_loader
    def load_user(user_id):
        return auth_User.query.get(int(user_id))

    return server