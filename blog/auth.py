from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        print(data)
        email = data.get("email")
        password_1 = data.get("password-1")
        print(email, password_1)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password_1):
                flash("Logged in!")
                print("Logged in!")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect", category="error")
                print("Password is incorrect", "error")
        else:
            flash("User does not exist", category="error")
            print("User does not exist", "error")
    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        email = data.get("email")
        password_1 = data.get("password-1")
        password_2 = data.get("password-2")
        first_name = data.get("password-2")
        last_name = data.get("password-2")
        print(data)
        if password_1 != password_2:
            flash("Passwords don/'t match", category="error")
        else:
            user = User(
                email=email,
                username=username,
                password=generate_password_hash(password_1, "sha256"),
                first_name=first_name,
                last_name=last_name,
            )
            try:
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                flash("Username or Email already in user", "error")
                print(f"An Error occurred {e}")
            else:
                login_user(user, remember=True)
                flash("Account Created Successfully.")
                return redirect(url_for("views.home"))

    return render_template("register.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
