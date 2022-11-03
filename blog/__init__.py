from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
db = SQLAlchemy()

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, BlogPost

    create_database(app)

    login_manager = LoginManager() # handles session for users 
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        with app.app_context():
            return User.query.get(int(id))

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    return app

def create_database(app):
    if not os.path.exists("blog/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database created")