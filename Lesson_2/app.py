from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path, PurePath
from re import split

# Создать страницу, на которой будет кнопка "Нажми меня", при
# нажатии на которую будет переход на другую страницу с
# приветствием пользователя по имени

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


# front-controller
@app.context_processor
def menu():
    menu_items = [
        {'name': 'Home', 'url': url_for('index')},
        {'name': 'task_1', 'url': url_for('task_1')},
        {'name': 'task_2', 'url': url_for('task_2')},
        {'name': 'task_3', 'url': url_for('task_3')},
        {'name': 'task_4', 'url': url_for('task_4')},
        {'name': 'task_5', 'url': url_for('task_5')},
        {'name': 'task_6', 'url': url_for('task_6')},
        {'name': 'task_7', 'url': url_for('task_7')},
        {'name': 'task_8', 'url': url_for('task_8')}
    ]
    return dict(menu_items=menu_items)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/task_1', methods=['GET', 'POST'])
def task_1():
    if request.method == 'POST':
        return redirect(url_for('hello', name='user'))
    return render_template('task_1.html')


@app.route('/task_2')
def task_2():
    return render_template('task_2.html')


@app.route('/task_2_upload', methods=['GET', 'POST'])
def task_2_upload():
    if request.method == 'POST':
        image = request.files.get('image')
        filename = secure_filename(image.filename)
        Path(Path.cwd(), 'static', 'uploads').mkdir(exist_ok=True)
        image.save(PurePath.joinpath(Path.cwd(), 'static', 'uploads', filename))
        return f"{filename} upload<br><a href='{url_for('task_2_upload')}'>back</a>"
    return render_template('form_task_2.html')


@app.route('/task_3', methods=['GET', 'POST'])
def task_3():
    login = 'l'
    passwd = 'p'
    if request.method == 'POST':
        log = request.form.get('login')
        pswd = request.form.get('password')
        if login == log and passwd == pswd:
            return redirect(url_for('hello', name=login))
        else:
            flash('Error', category='danger')
            return redirect(url_for('task_3'))
    return render_template('task_3.html')


@app.route('/task_4', methods=['GET', 'POST'])
def task_4():
    if request.method == 'POST':
        text = request.form.get('text').strip()
        words = split(r'[,.\s]+', text)
        return f"{len(words)} words"
    return render_template('task_4.html')


@app.route('/task_5', methods=['GET', 'POST'])
def task_5():
    if request.method == 'POST':
        result = None
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        op = request.form.get('operation')
        if op == 'plus':
            result = num1 + num2
        elif op == 'mult':
            result = num1 * num2
        elif op == 'div':
            result = num1 / num2 if num2 != 0 else 0
        else:
            result = num1 - num2
        return f"{num1} {op} {num2} = {result}"
    return render_template('task_5.html')


@app.route('/task_6', methods=['GET', 'POST'])
def task_6():
    if request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        if age >= 18:
            return render_template('index.html')
        else:
            return render_template('404.html')
    return render_template('task_6.html')


@app.route('/task_7', methods=['GET', 'POST'])
def task_7():
    if request.method == 'POST':
        num = int(request.form.get('num'))
        return f"{num ** 2}"
    return render_template('task_7.html')


@app.route('/task_8', methods=['GET', 'POST'])
def task_8():
    if request.method == 'POST':
        if not request.form.get('name'):
            flash('Name not enterd', 'danger')
            return redirect(url_for('task_8'))
        flash('OK', 'success')
        return redirect(url_for('hello', name=f"{request.form.get('name')}"))
    return render_template('task_8.html')


@app.route('/hello/<name>')
def hello(name):
    return f"Hello {name}"
