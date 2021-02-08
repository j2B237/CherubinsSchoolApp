from datetime import timedelta
from flask import (Blueprint, redirect, render_template, url_for, flash, request, abort)
from flaskr.forms import RegistrationForm, LoginForm
from flaskr import app, db, bcrypt, login_manager
from flask_login import current_user, login_user
from flaskr.models import User, Post, db_create


#Create a blueprint for the register and auth process
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST','GET'])

def register():

    db_create()
    form = RegistrationForm()
    # alors affiche la page de login
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()

        if username:
            flash("Nom d'utilisateur existe deja ! Choisissez un autre.", 'danger')
        elif email:
            flash("Email existe deja ! Choisissez un autre.", 'danger')

        else:
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
            db.session.add(user)
            db.session.commit()

            flash('Le compte {} a été créé avec succes'.format(form.username.data), 'success')
            return redirect(url_for('auth.login'))

    return abort(403, "Vous n'etes pas autorisé à accéder à cette page.")



@bp.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            checked_password = bcrypt.check_password_hash(user.password, form.password.data)
            if checked_password:
                login_user(user, remember=False)
                next_page = request.args.get('next')

                return redirect(next_page) if next_page else redirect(url_for('admin.index'))
            else:
                flash('Mot de passe incorrect', 'danger')
        else:
            flash('Mot de passe ou email incorrect', 'danger')

    return render_template('auth/login.html', title='ACCES RESERVE', form=form)

