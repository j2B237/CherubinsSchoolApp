from flask import Blueprint, render_template, flash, abort
from flaskr import db, mail
from flask_mail import Message
from flaskr.models import School, Post, Request_user, db_create
from flaskr.forms import ContactForm

bp = Blueprint('www', __name__)

test_school = {
    "name": "My school",
    "description": "My school est une école test qui sert de fake data.\
                    Tout ce dont l’enfant a besoin pour son épanouissement intégral est à sa disposition.\
                    Venez voir et sans nul doute, vous serez séduit par le décor.",
    "date_posted": "22/02/2021",
    "address": "OUAKAM DAKAR"
}

testPosts = [
    {
        'title': 'First post',
        'content': 'This is my first post'
     },

    {
        'title': 'Second post',
        'content': 'This is my second post',
    },

    {
        'title': 'Third post',
        'content': 'This is my third post',
    }

]

@bp.route('/')
def index():
    try:
        db_create()
    except:
        print('Error creating Database')

    my_school = School.query.filter_by(admin_id=1).first()
    #Toujours ecrire la requete dans cet ordre
    posts = Post.query.filter_by(user_id=1).order_by(Post.date_posted.desc()).limit(3)
    if my_school is None:
        return render_template('www/index.html',
                               title="Ecole Maternelle | Primaire | {}".format(test_school["name"]),
                               school=test_school,
                               posts=testPosts
                               )

    return render_template('www/index.html',
                           title="Ecole Maternelle | Primaire | {}".format(my_school.name),
                           school=my_school,
                           posts=posts)

@bp.route('/la-maternelle')
def edit_maternelle():
    my_school = School.query.filter_by(admin_id=1).first()
    if not my_school:
        return render_template('www/maternelle.html', title="{}".format(test_school.name), school=test_school)
    return render_template('www/maternelle.html', title="{}".format(my_school.name), school=my_school)

@bp.route('/le-primaire')
def edit_primaire():
    my_school = School.query.filter_by(admin_id=1).first()
    if not my_school:
        return render_template('www/primaire.html', title="{}".format(test_school.name), school=test_school)

    return render_template('www/primaire.html', title="{}".format(my_school.name), school=my_school)

@bp.route('/les-services')
def edit_services():
    my_school = School.query.filter_by(admin_id=1).first()
    if not my_school:
        return render_template('www/services.html', title="Service - {}".format(test_school.name), school=test_school)
    return render_template('www/services.html', title="Services - {}".format(my_school.name), school=my_school)

@bp.route('/actualites')
def edit_actualite():
    my_school = School.query.filter_by(admin_id=1).first()
    posts = Post.query.filter_by(user_id=1).order_by(Post.date_posted.desc()).all()
    if not my_school:
        return render_template('www/actualités.html', title="Actualités - {}".format(test_school.name), school=test_school, posts=testPosts)
    return render_template('www/actualités.html', title="Actualités - {}".format(my_school.name), school=my_school, posts=posts)

@bp.route('/actualités/post/<int:post_id>')
def view_post(post_id):
    my_school = School.query.filter_by(admin_id=1).first()
    post = Post.query.get(post_id)
    posts = Post.query.all()

    if not my_school:
        return render_template('www/post.html', title="Actualités - {}".format(test_school.name), school=test_school,
                               post=testPosts[1],
                               posts=testPosts)

    return render_template('www/post.html', title="Actualité",
                           school=my_school,
                           post=post,
                           posts=posts)

@bp.route('/mediatheque')
def edit_mediatheque():
    my_school = School.query.filter_by(admin_id=1).first()
    if not my_school:
        return render_template('www/mediatheque.html', title="Médiathèque - {}".format(test_school.name), school=test_school)

    return render_template('www/mediatheque.html', title="Médiathèque - {}".format(my_school.name), school=my_school)


@bp.route('/contact', methods=['POST','GET'])
def contact():
    my_school = School.query.filter_by(admin_id=1).first()
    db_create()
    form = ContactForm()
    flash_message = None
    category = None

    if not my_school:
        return render_template('www/contact.html', title="Contact - {}".format(test_school.name),
                               school=test_school,
                               form=form)

    if form.validate_on_submit():

        user = form.username.data
        contact = form.phone_number.data
        message = form.message.data

        #Recherche si un utilisateur correspond à cette requete
        search_user = Request_user.query.filter_by(username=user).first()
        search_contact = Request_user.query.filter_by(contact=contact).first()

        if search_user or search_contact:
           flash_message = 'Une demande a deja été envoyée à ce nom ou avec ce numéro'
           category = 'info'

        else:
            try:
                #Insert request
                request = Request_user(username=user, contact=contact, message=message)
                db.session.add(request)
                db.session.commit()

                #Send admin user request
                user = form.username.data
                contact = form.phone_number.data
                user_msg = form.message.data

                msg = Message('Nouvelle demande de contact', sender='b.bj03@outlook.fr', recipients=['contact@digitalschools.sn'])
                msg.body = user_msg + " Contact : {} / {} ".format(user, contact)
                mail.send(msg)
            except:
                pass

            flash_message = 'Votre demande a bien été transmise, nous vous contacterons très bientot'
            category = 'success'

        flash(flash_message, category)

    return render_template('www/contact.html',title='Contact - Les Chérubins',
                           school=my_school,
                           form=form)