from datetime import timedelta
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

"Application factory"
# create flask object
app = Flask(__name__)

#APPLICATION CONFIGURATION
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SECRET_KEY'] = 'random_string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=0, hours=0, minutes=5, seconds=0, milliseconds=0)
app.config['SESSION_PROTECTION'] = "strong"

#Configuration server Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'user@gmail.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = False

mail = Mail(app)

#Create SQLAlchemy object
db = SQLAlchemy(app)

#Encryption user's password
bcrypt = Bcrypt(app)

#Login management
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'
login_manager.login_message = " Veuillez vous authentifier afin d'accéder à cette page"
login_manager.login_message_category = 'info'

#In addition to verify that the user is logged in
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = (
    "Pour proteger votre compte, veuillez-vous connecter afiin d'accéder à cette page")
login_manager.needs_refresh_message_category = "info"

# create a simple hello page for test
@app.route('/hello')
def hello():
    return "HELLO FLASK APP !!"

from . import auth
app.register_blueprint(auth.bp)

from . import admin
app.register_blueprint(admin.bp)

from . import www
app.register_blueprint(www.bp)
app.add_url_rule('/', endpoint='index')
