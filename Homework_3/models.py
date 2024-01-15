from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    passwd = db.Column(db.BINARY, nullable=False)
    surname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female'))
    group = db.Column(db.Enum('A', 'B', 'C'))
    email = db.Column(db.String(100))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    birthday = db.Column(db.String(80))
    terms = db.Column(db.Boolean)

    def __repr__(self):
        return f'User({self.surname} {self.name} - group {self.group})'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user = db.relationship('User', backref='faculty', lazy=True)

    def __repr__(self):
        return f'Faculty({self.name})'


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_name = db.Column(db.String(100))
    mark = db.Column(db.Integer)
    user = db.relationship('User', backref='marks', lazy=True)
