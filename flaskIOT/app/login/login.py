from sqlalchemy import update
from flask import request, Blueprint, session, redirect, jsonify
from os import getenv
from app.database.tables import *
from app.database.__init__ import db
from ..utils.utils import Utils
from flask import render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.login.__init__ import bcrypt, login_manager

login_blueprint = Blueprint(
    "login", __name__, template_folder="templates", url_prefix="/login"
)

SECRET_KEY = getenv("SECRET_KEY")
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_blueprint.route("/")
def home():
    return render_template('home.html')


#USER

@login_blueprint.route('/userhome', methods=['GET', 'POST'])
def userhome():
    return render_template('userhome.html')

@login_blueprint.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    form = LoginFormUser()

    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('login.dashboarduser'))
        """
        if admin:
            if bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin)
                return redirect(url_for('login.dashboard'))
        """

    return render_template('login_user.html', form=form)

@login_blueprint.route('/dashboarduser', methods=['GET', 'POST'])
@login_required
def dashboarduser():
    return render_template('dashboarduser.html')

@login_blueprint.route('/logoutuser', methods=['GET', 'POST'])
@login_required
def logoutuser():
    logout_user()
    return redirect(url_for('login.loginuser'))

@ login_blueprint.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    form = RegisterFormUser()
    if form.validate_on_submit():
        new_user = User(
                Person(
                    username=form.username.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    password=bcrypt.generate_password_hash(form.password.data, 10).decode('utf-8'), 
                    city=form.city.data,
                    birth_year=form.birth_year.data,
                    card_number=form.card_number.data
                ),
                form.apartment_name.data,
                form.internal_number.data,
            )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login.loginuser'))

    return render_template('register_user.html', form=form)

#OPERATOR
@login_blueprint.route('/operatorhome', methods=['GET', 'POST'])
def operatorhome():
    return render_template('operatorhome.html')

@ login_blueprint.route('/registeroperator', methods=['GET', 'POST'])
def registeroperator():
    form = RegisterFormOperator()
    if form.validate_on_submit():
        new_user = Operator(
                Person(
                    username=form.username.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    password=bcrypt.generate_password_hash(form.password.data, 10).decode('utf-8'),  
                    city=form.city.data,
                    birth_year=form.birth_year.data,
                    card_number=form.card_number.data
                ),
                form.id_operator.data,
            )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login.loginoperator'))

    return render_template('register_operator.html', form=form)

@login_blueprint.route('/loginoperator', methods=['GET', 'POST'])
def loginoperator():
    form = LoginFormOperator()

    if form.validate_on_submit():
        operator = Operator.query.filter(Operator.username==form.username.data).first()
    
        """
        if admin:
            if bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin)
                return redirect(url_for('login.dashboard'))
        """
        if operator:
            if bcrypt.check_password_hash(operator.password, form.password.data):
                login_user(operator)
                return redirect(url_for('login.dashboardoperator'))
    return render_template('login_operator.html', form=form)

@login_blueprint.route('/dashboardoperator', methods=['GET', 'POST'])
@login_required
def dashboardoperator():
    return render_template('dashboardoperator.html')

@login_blueprint.route('/logoutoperator', methods=['GET', 'POST'])
@login_required
def logoutoperator():
    logout_user()
    return redirect(url_for('login.loginoperator'))

def generate_password(password):
    return bcrypt.generate_password_hash(password, 10).decode('utf-8')