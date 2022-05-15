from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'site.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'potestuff'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialise our db
    db.init_app(app)

    # import our blueprints
    from .auth import auth
    from .main import main
    # registering blueprints
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')

    # import our db object classes
    from .models import User, Blog, Comment

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# create our db
def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Database has been created')