from flask import Flask, render_template, redirect, request, url_for, flash, session
import secrets
from re import match

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.get('/identification')
def identification_get():
    return render_template('identification.html')


@app.post('/identification')
def identification_post():
    name = request.form.get('name')
    email = request.form.get('email')
    if name.isalpha() and match(r'.*@\w*\.\w{2,3}', email):
        session['client'] = name
        session['email'] = email
        return redirect(url_for('home'))
    flash('Wrong name or email', 'danger')
    return redirect(url_for('identification_get'))


@app.route('/logout')
def logout():
    session.pop('client')
    session.pop('email')
    return redirect(url_for('identification_post'))


@app.route('/')
@app.route('/index.html')
@app.route('/home')
def home():
    client = session.get('client')
    if client:
        return render_template('index.html', **dict(client=client))
    else:
        return redirect(url_for('identification_post'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(error):
    return render_template('505.html')
