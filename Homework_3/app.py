from flask import Flask, url_for, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
import secrets

from models import User, db
from forms import LoginForm, RegistrationForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homework3.db"
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

csrf = CSRFProtect()
db.init_app(app)
migrate = Migrate(app, db)
crypt = Bcrypt(app)

csrf.init_app(app)


@app.context_processor
def navigation():
    menu = [
        {"name": "Home", "uri": url_for("home")},
        {"name": "Login", "uri": url_for("log_in")},
        {"name": "Registration", "uri": url_for("registration")}
    ]
    return dict(menu=menu)


@app.route('/')
def home():
    log = session.get("name", "Please login")
    return render_template("index.html", login=log)


@app.route("/login", methods=["GET", "POST"])
def log_in():
    form = LoginForm()
    username = form.name.data
    email = form.email.data
    password = form.password.data
    if request.method == "POST" and form.validate():
        user = User.query.filter(User.name == username, User.email == email).first()
        try:
            if crypt.check_password_hash(bytes(user.passwd), password):
                session["name"] = form.name.data
                return redirect(url_for("home"))
            raise ValueError("Wrong password")
        except (ValueError, AttributeError) as err:
            return render_template("login.html", form=form, alert_message=err)
    return render_template("login.html", form=form)


@app.route("/logout")
def log_out():
    session.pop("name")
    return redirect(url_for("home"))


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    username = form.name.data
    email = form.email.data
    if request.method == "POST" and form.validate():
        if User.query.filter(User.name == username, User.email == email).all():
            return render_template("registration.html", form=form,
                                   alert_message="User already exist!")

        # При отправке формы данные должны сохраняться в базе данных,
        # а пароль должен быть зашифрован.
        session["name"] = form.name.data
        new_user = User(name=username, email=email,
                        passwd=crypt.generate_password_hash(form.password.data),
                        birthday=form.birthday.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("registration.html", form=form)
