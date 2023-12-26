from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<name>')
def hello(name):
    return f"<h1>hello from flask {name}</h1>"


@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/add-nums/<int:num>/<int:num2>')
def add_nums(num, num2):
    return str(num + num2)


@app.route('/students')
def students():
    _students = [
        {
            'name': 'Maksim',
            'surname': 'Doe',
            'age': 33,
            'average': 15_000
        },
        {
            'name': 'Andrey',
            'surname': 'Gro',
            'age': 35,
            'average': 20_000
        }
    ]
    context = {'students': _students}
    return render_template('students.html', **context)
