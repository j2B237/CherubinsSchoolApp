from flask import (Blueprint, redirect, render_template, url_for, flash, request, abort)
from sqlalchemy import desc
from flask_login import login_required, logout_user, login_user, current_user
from flaskr import db, mail
from flask_mail import Message
from flaskr.models import (School, Post,
                            Cycle, OpenedDays,
                            Service, Role,
                            Request_user, Personnel)

from flaskr.forms import (PostForm, SchoolForm, CycleForm,
                            OpenedDaysForm, ServiceForm,
                            RoleForm, PersonnelForm, ContactPersonnelForm)


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
def index():
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()
    requests = Request_user.query.count()
    params = School.query.count()
    n = Post.query.count()
    persons = Personnel.query.filter_by(school_id=school.id).count()
    return render_template('admin/index.html',
                           title='Administration - Les Cherubins',
                           school=school,
                           posts=int(n),
                           requests=int(requests),
                           persons=int(persons),
                           params=int(params)
                           )


@bp.route('/post/create', methods=['POST','GET'])
@login_required
def create():
    params = School.query.count()
    form = PostForm()
    msg = None
    category = None

    if form.validate_on_submit():
        title = form.title.data
        content = form.message.data
        user_id = current_user.id

        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()

        msg = "L'article a bien été créé "
        category = 'success'

        return redirect(url_for('admin.index'))

        flash(msg, category)

    flash('')
    return render_template('admin/create_post.html',
                           title='Administration - Les Cherubins',
                           form=form,
                           params=int(params))


@bp.route('/post/<int:post_id>')
@login_required
def post(post_id):
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()
    post = Post.query.get_or_404(post_id)

    return render_template("admin/post.html", title="Administration {}".format(school.name),
                           params=params,
                           post=post)


@bp.route('/update/post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()

    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.message.data
        db.session.commit()
        flash("L'article a été modifié avec succès", "success")
        return redirect(url_for('admin.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.message.data = post.content

    return render_template("admin/update_post.html", title="Administration - {}".format(school.name),
                           params=params,
                           form=form
                           )

@bp.route('/delete/post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("L'article a été supprimé avec succes", "success")

    return redirect(url_for('admin.list_post'))

@bp.route('/post')
@login_required
def list_post():
    params = School.query.count()
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
    return render_template('admin/list_post.html',
                           title='Administration - MySchool',
                           params=int(params),
                           posts=posts)


@bp.route('/configure')
@login_required
def configure():
    params = School.query.count()
    return render_template('admin/configuration.html', title= 'Configuration',
                           params=int(params))


@bp.route('/configure/school', methods=['POST', 'GET'])
@login_required
def school_config():
    params = School.query.count()
    form = SchoolForm()
    if form.validate_on_submit():

        #Capture form data
        name = form.name.data
        description = form.description.data
        address = form.address.data
        email = form.email.data
        phone = form.phone_number.data
        website = form.web.data
        admin_id = current_user.id

        #Vérification si les données saisies correspondent à une entrée dans la DB
        res = School.query.filter_by(name=name).first_or_404()
        if res:
            flash("Une école de ce nom existe deja", "danger")
        else:

            school = School(name=name, description=description,
                        address=address,email=email,
                        phone_number=phone, website_url=website,
                        admin_id=admin_id
                        )
            db.session.add(school)
            db.session.commit()
            flash("Votre établissement a bien été enrégistré. Maintenant vous pouvez configurer les autres paramètres.", 'success')
            return redirect(url_for('admin.school_config'))

    return render_template('admin/school_config.html', title= 'Configuration',
                           params=int(params),
                           form=form)


@bp.route('/school/edit', methods=['POST', 'GET'])
@login_required
def edit_school():
    params = School.query.count()
    form = SchoolForm()

    school = School.query.filter_by(admin_id=current_user.id).first()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        address = form.address.data
        email = form.email.data
        phone_number = form.phone_number.data
        web = form.web.data

        school.name = name
        school.description = description
        school.address = address
        school.email = email
        school.phone_number = phone_number
        school.website_url = web
        school.admin_id = current_user.id

        db.session.commit()
        flash("Paramétres établissement mis à jour avec succès", "success")
        return redirect(url_for("admin.etablissement"))

    elif request.method == 'GET':
        # Update
        form.name.data = school.name
        form.description.data = school.description
        form.address.data = school.address
        form.email.data = school.email
        form.phone_number.data = school.phone_number
        form.web.data = school.website_url


    return render_template('admin/edit_school.html',
                           title='Configuration Ecole',
                           params=int(params),
                           form=form)


@bp.route('/configure/heures-ouverture', methods=['POST', 'GET'])
@login_required
def opened_hours():
    params = School.query.count()

    form = OpenedDaysForm()
    msg = None
    category = None

    if form.validate_on_submit():
        # recherche l'école qui est administrée
        school = School.query.filter_by(admin_id=current_user.id).first()

        #Crée 7 jours  à partir des données capturées du formulaire
        day1 = {"name": "Lundi","hours": form.day1.data}
        day2 = {"name": "Mardi","hours": form.day2.data}
        day3 = {"name": "Mercredi","hours": form.day3.data}
        day4 = {"name": "Jeudi","hours": form.day4.data}
        day5 = {"name": "Vendredi","hours": form.day5.data}
        day6 = {"name": "Samedi","hours": form.day6.data}
        day7 = {"name": "Dimanche","hours": form.day7.data}

        days = [day1, day2, day3, day4, day5, day6, day7]

        for day in days:
            #Pour chaque créé une instance et insere dans la DB
            if day['hours'] != "":
                #Recherche un jour de semaine si existe deja
                search_day = OpenedDays.query.filter_by(dayName=day['name']).first()
                if search_day:
                    msg = "Impossible d'ajouter ce jour d'ouverture"
                    category = "danger"
                else:
                    #Ajouter le jour s'il n'existe pas
                    d = OpenedDays(dayName=day['name'], dayHours=day['hours'], school_id=school.id)
                    db.session.add(d)
                    msg = "Les heures d'ouverture ont bien été enrégistrées."
                    category = "success"
        #Affiche un message selon le type de categorie
        flash(msg, category)
        db.session.commit()

        return redirect(url_for('admin.opened_hours'))

    return render_template('admin/Hours_config.html',
                           title='Configuration',
                           params=params,
                           form=form)


@bp.route('/configure/cycles', methods=['POST', 'GET'])
@login_required
def cycle_config():
    params = School.query.count()
    form = CycleForm()

    if form.validate_on_submit():
        msg = None
        category = None

        # recherche l'école qui est administrée
        school = School.query.filter_by(admin_id=current_user.id).first_or_404()

        name = form.designation.data
        description = form.description.data

        #Verifier si un cycle avec ce nom existe
        search_cycle = Cycle.query.filter_by(designation=name).first_or_404()
        if search_cycle:
            msg = "Impossible d'ajouter ce cycle"
            category = "danger"
        else:
            cycle = Cycle(designation=name, description=description, school_id=school.id)
            db.session.add(cycle)
            db.session.commit()
            msg = "Le cycle a bien été ajouté"
            category = "success"

        flash(msg, category)
        return redirect(url_for('admin.cycle_config'))

    return render_template('admin/cycle_config.html',
                           title='Configuration',
                           params=int(params),
                           form=form)

@bp.route('/configure/services', methods = ['POST', 'GET'])
@login_required
def service_config():
    params = School.query.count()
    form = ServiceForm()

    if form.validate_on_submit():
        msg = None
        category = None
        # recherche l'école qui est administrée
        school = School.query.filter_by(admin_id=current_user.id).first_or_404()

        name = form.designation.data
        description = form.description.data

        search_service = Service.query.filter_by(designation=name).first_or_404()

        if search_service:
            msg = "Impossible d'ajouter ce service"
            category = "danger"
        else:
            service = Service(designation=name, description=description, school_id=school.id)
            db.session.add(service)
            db.session.commit()
            msg = "Le service a bien été ajouté"
            category = "success"

        flash(msg, category)
        return redirect(url_for('admin.service_config'))

    return render_template('admin/services_config.html',
                           title='Configuration',
                           params=params,
                           form=form
                           )


@bp.route('/configure/roles', methods=['POST', 'GET'])
@login_required
def role_config():
    params = School.query.count()
    form = RoleForm()

    if form.validate_on_submit():
        msg = None
        category = None
        name = form.designation.data
        search_role = Role.query.filter_by(designation=name).first_or_404()

        if search_role:
            msg = "Impossible d'ajouter ce role"
            category = "danger"
        else:
            role = Role(designation=name)
            db.session.add(role)
            db.session.commit()
            msg = "Le role a bien été ajouté"
            category = "success"

        flash(msg, category)
        return redirect(url_for('admin.role_config'))

    return render_template('admin/role_config.html',
                           title='Configuration',
                           params=params,
                           form=form
                           )

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('www.index'))


#DISPLAY OTHERS TABS

@bp.route('/etablissement')
@login_required
def etablissement():
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()
    roles = Role.query.all()
    return render_template('admin/etablissement.html',
                           title='Dashboard - Etablissement',
                           school=school,
                           roles=roles,
                           params=int(params))

@bp.route('/requests-user')
@login_required
def request_user():
    params = School.query.count()
    requests = Request_user.query.order_by(Request_user.date_posted.desc()).all()
    return render_template('admin/requests.html',
                           title='Administration - MySchool',
                           requests=requests,
                           params=int(params))
@bp.route('/request-user/<int:request_id>', methods=['POST', 'GET'])
@login_required
def view_request_user(request_id):
    return "VIEW REQUEST USER id={}".format(request_id)

@bp.route('/create/employee', methods=['POST', 'GET'])
@login_required
def create_employee():

    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()
    roles = Role.query.all()
    form = PersonnelForm()
    msg = None
    category = None

    if form.validate_on_submit():

        name = form.username.data
        email = form.email.data
        phone = form.phone_number.data
        role = request.form['role']
        search_role = Role.query.filter_by(designation=role).first()

        #recherche employee
        search_name = Personnel.query.filter_by(username=name).first()
        search_email = Personnel.query.filter_by(email=email).first()
        search_phone = Personnel.query.filter_by(phone_number=phone).first()

        if search_name:
            msg = "Cet employé existe déja"
            category = "danger"
        elif search_email:
            msg = "Cet email existe déja"
            category = "danger"
        elif search_phone:
            msg = "Cet numéro de téléphone existe déja"
            category = "danger"
        else:
            employee = Personnel(username=name,
                                 email=email,
                                 phone_number=phone,
                                 role_id=search_role.id,
                                 school_id=school.id)
            db.session.add(employee)
            db.session.commit()

            msg ="Employé créé avec success"
            category = "success"

        flash(msg, category)
        return redirect(url_for('admin.create_employee'))


    return render_template('admin/create_employee.html', title="Administration - MyScholl",
                           params=params,
                           form=form,
                           roles=roles)


@bp.route('/employee/<int:employee_id>')
@login_required
def employee_profil(employee_id):
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()

    employee = Personnel.query.get_or_404(employee_id)

    return render_template('admin/employee.html', title="Administration - {}".format(school.name),
                           employee=employee,
                           params=params,
                           school=school
                           )


@bp.route('contact/employee/<int:employee_id>', methods=['POST','GET'])
@login_required
def contact_employee(employee_id):
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()

    employee = Personnel.query.get_or_404(employee_id)
    form = ContactPersonnelForm()

    if form.validate_on_submit():
        sender = form.sender.data
        receiver = form.recipient.data
        message = form.message.data
        objet = form.Object.data

        msg = Message(objet, recipients=[receiver], sender=sender)
        msg.body = message
        mail.send(msg)

        flash("Message envoyé", "success")
        return redirect(url_for('admin.employee_profil', employee_id=employee.id))

    elif request.method == 'GET':
        form.sender.data = "contact@digitalschools.sn"
        form.recipient.data = employee.email


    return render_template('admin/contact_employee.html',
                           employee=employee,
                           form=form,
                           params=params)


@bp.route('update/profil-employee/<int:employee_id>', methods=['POST', 'GET'])
@login_required
def update_employee(employee_id):
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()
    roles = Role.query.all()

    flash_msg = None
    category = None

    employee = Personnel.query.get_or_404(employee_id)

    if employee.school_id != school.id:
        abort(403)

    form = PersonnelForm()

    if form.validate_on_submit():

        employee.username = form.username.data
        employee.email = form.email.data
        employee.phone_number = form.phone_number.data

        role = form.role.data
        search_role = Role.query.filter_by(designation=role).first()
        employee.role_id = search_role.id

        db.session.commit()

        flash_msg = "Profil mis à jour avec succès"
        category = "success"

        flash(flash_msg, category)
        return redirect(url_for('admin.employee_profil', employee_id=employee.id))

    elif request.method == 'GET':
        form.username.data = employee.username
        form.email.data = employee.email
        form.phone_number.data = employee.phone_number
        role = Role.query.get_or_404(employee.role_id)

        form.role.data = role

    return render_template("admin/update_employee.html", title="Administration - {}".format(school.name),
                           form=form,
                           employee=employee,
                           params=params,
                           roles=roles)


@bp.route('/employees')
@login_required
def list_employee():
    params = School.query.count()
    school = School.query.filter_by(admin_id=current_user.id).first_or_404()
    employees = Personnel.query.all()

    return render_template('admin/list_employees.html', title="Administration - {}".format(school.name),
                           employees=employees,
                           params=params)