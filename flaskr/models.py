from datetime import datetime
from flaskr import db, app, login_manager
from flask_login import UserMixin


def db_create():
    db.create_all()

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    address = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    website_url = db.Column(db.String(30), unique=True, nullable=True)
    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    OpenedHours = db.relationship('OpenedDays', backref='school', lazy=True)
    cycles = db.relationship('Cycle', backref='school', lazy=True)
    services = db.relationship('Service', backref='school', lazy=True)
    personnels = db.relationship('Personnel', backref='school', lazy=True)

    def __repr__(self):
        return "< School : {}, {}, {}, {}, {}>" .format(self.name, self.address,
                                                        self.OpenedHours, self.cycles, self.services)


class OpenedDays(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dayName = db.Column(db.String(20), nullable=False, unique=True)
    dayHours = db.Column(db.String(20), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

    def __repr__(self):
        return "< OpenedDays: {}, {}".format(self.dayName, self.dayHours)


class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    documents = db.relationship('Document', backref='cycle', lazy=True)

    def __repr__(self):
        return "<Cycle : {}, {}".format(self.designation, self.description)



class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

    def __repr__(self):
        return "< Service : {}, {}".format(self.designation, self.description)



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(80), nullable=False)
    personnels = db.relationship('Personnel', backref='role', lazy=True)

    def __repr__(self):
        return "<Role : {} - ({})".format(self.designation, self.personnels)



class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    image_file = db.Column(db.String(50), default='default.jpg')
    hired_at = db.Column(db.DateTime, default=datetime.utcnow())
    fired_On = db.Column(db.DateTime, nullable=True)
    still_Working = db.Column(db.BOOLEAN, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

    def __repr__(self):
        return "<Personnel : {} - {} - {} ".format(self.username, self.role, self.phone_number)



class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'), nullable=False)

    def __repr__(self):
        return "Document : {} - {}, {}".format(self.title, self.cycle, self.description)



class Request_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return "<Demande de contact : {}, {}".format(self.username, self.contact)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User {} {} {}".format(self.username, self.email, self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    displayed_Or_Not = db.Column(db.BOOLEAN, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "User {} {}".format(self.title, self.date_posted)



