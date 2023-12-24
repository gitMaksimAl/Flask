from flask import Flask, render_template, current_app

app = Flask(__name__, root_path='/home/Maksim/GB3474/Flask/Homework_1')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/Clothes')
def clothes():
    _clothes = {
            'jacket': {
                'description': 'Cool jacket for summer',
                'size': 'M',
                'color': 'braun',
                'price': 12.99
            },
            'pants': {
                'description': 'Modern yellow pants',
                'size': 'M',
                'color': 'green',
                'price': 10.99
            },
            'hat': {
                'description': 'Red hat',
                'size': 'M',
                'color': 'red',
                'price': 9.99
            }
    }
    content = {'clothes': _clothes}
    return render_template('clothes.html', **content)


@app.route('/Clothes/<item>')
def clothes_item(item):
    return render_template('item.html')


@app.route('/Shoes')
def shoes():
    _shoes = {
        'boots': {
            'description': 'Nice for riding',
            'size': 'M',
            'color': 'black',
            'price': 15.55
        },
        'slates': {
            'description': 'Nice for gazellist',
            'size': 'M',
            'color': 'green',
            'price': 2.33
        }
    }
    content = {'shoes': _shoes}
    return render_template('shoes.html', **content)


@app.route('/Shoes/<item>')
def shoes_item(item):
    return render_template('item.html')

@app.route('/Info')
def config():
    _config = app.config
    context = {'config': _config}
    return render_template('info.html', **context)


@app.route('/Contact')
def contact():
    _contact = {
        'Andrey': {
            'phone': '9165152211',
            'email': 'andrey@google.com'
        },
        'Arseni': {
            'phone': '9168184433',
            'email': 'arseni@google.com'
        },
        'Sergey': {
            'phone': '9167173322',
            'email': 'sergey@google.com'
        }
    }
    context = {'contacts': _contact}
    return render_template('contact.html', **context)
