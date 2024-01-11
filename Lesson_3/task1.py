from flask import Flask, url_for, render_template, request
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import secrets

from models import Student, Book, Mark
from models import db
from forms import LoginForm
from forms import RegistrationForm

app = Flask(__name__)
csrf = CSRFProtect()
migrate = Migrate()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lesson3.db"
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
csrf.init_app(app)
db.init_app(app)
migrate.init_app(app, db)


@app.context_processor
def menu_items():
    menu = [
        {"name": "Home", "uri": url_for("index")},
        {"name": "Students", "uri": url_for("all_students")},
        {"name": "Books", "uri": url_for("all_books")},
        {"name": "Login", "uri": url_for("login")},
        {"name": "Registration", "uri": url_for("registration")}
    ]
    return dict(menu=menu)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Students")
def all_students():
    studs = Student.query.order_by(-Student.id).all()
    return render_template("task1.tpl", students=studs)


@app.route("/Books")
def all_books():
    books = Book.query.all()
    return render_template("task2.tpl", books=books)


@app.route("/Students/Marks")
def all_marks():
    students = Student.query.all()
    student_data = []

    for student in students:
        marks = Mark.query.filter_by(student_id=student.id).all()
        mark_data = [{'subject_name': mark.subject_name,
                      'mark': mark.mark} for mark in marks]
        student_info = {
            'id': student.id,
            'name': student.name,
            'surname': student.surname,
            'age': student.age,
            'gender': student.gender,
            'group': student.group,
            'email': student.email,
            'marks': mark_data
        }
        student_data.append(student_info)
        return render_template("task3.tpl", student_data=student_data)


@app.route('/Login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    context = {}
    if request.method == 'POST' and form.validate():
        if Student.query.filter(
                Student.name == username).all() and \
                Student.query.filter(Student.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('login.html', form=form, **context)
        else:
            new_user = Student(name=username, email=email)
            new_user.password = password
            db.session.add(new_user)
            db.session.commit()
            context = {'alert_message': "Пользователь добавлен!"}
    return render_template('login.html', form=form, **context)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    context = {'alert_message': "Добро пожаловать!"}
    form = RegistrationForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    birthday = form.birthday.data
    terms = form.terms.data
    if request.method == 'POST' and form.validate():
        if Student.query.filter(Student.name == username).all() and \
                Student.query.filter(Student.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('registration.html', form=form, **context)
        else:
            new_user = Student(name=username, email=email, birthday=birthday,
                               terms=terms)
            new_user.password = password
            db.session.add(new_user)
            db.session.commit()
            return render_template('registration.html', form=form, **context)
    return render_template('registration.html', form=form)
