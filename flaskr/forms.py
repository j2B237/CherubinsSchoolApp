from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo


class RegistrationForm(FlaskForm):

    username = StringField('nom utilisateur',
                           validators=[DataRequired(), Length(2, 20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Mot de passe',
                             validators=[DataRequired(), Length(8, 50), ])

    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), Length(8, 50), EqualTo('password')])

    submit = SubmitField('Enregistrer')



class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe',
                             validators=[DataRequired(), Length(8, 50), ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Connexion')



class ContactForm(FlaskForm):

    username = StringField('Votre nom', validators=[DataRequired()])
    phone_number = StringField('Votre téléphone', validators=[DataRequired()])
    message = TextAreaField('Votre message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class ContactPersonnelForm(FlaskForm):
    sender = StringField('De :', validators=[Email()])
    recipient = StringField('A :', validators=[Email()])
    Object = StringField('Objet')
    message = TextAreaField('Votre message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class PostForm(FlaskForm):

    title = StringField('Titre', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class SchoolForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    phone_number = StringField('Telephone', validators=[Length(9, 13)])
    web = StringField('Website')

    submit = SubmitField('Enregistrer')

class OpenedDaysForm(FlaskForm):
    day1 = StringField('Lundi')
    day2 = StringField('Mardi')
    day3 = StringField('Mercredi')
    day4 = StringField('Jeudi')
    day5 = StringField('Vendredi')
    day6 = StringField('Samedi')
    day7 = StringField('Dimanche')

    submit = SubmitField('Valider')


class CycleForm(FlaskForm):
    designation = StringField('Designation', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class ServiceForm(FlaskForm):
    designation = StringField('Designation', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class RoleForm(FlaskForm):
    designation = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Valider')


class PersonnelForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    phone_number = StringField('Telephone', validators=[Length(9, 13)])
    role = StringField('Role', validators=[DataRequired()])

    submit = SubmitField('Enregistrer')