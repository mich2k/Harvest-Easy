from flask import request, Blueprint, session, jsonify
from os import getenv
from app.database.tables import *
from app.database.__init__ import db
from ..utils.utils import Utils
from app.login.__init__ import bcrypt


login_blueprint = Blueprint(
    "login", __name__, template_folder="templates", url_prefix="/login"
)

@login_blueprint.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


@login_blueprint.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "city": user.city,
        "internal_number": user.internal_number,
        "birth_year": user.birth_year,
        "card_number": user.card_number,
        "apartment_ID": user.apartment_ID
    }) 


#USER

@login_blueprint.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    msgJson = request.get_json()
    password = msgJson["password"]
    username = msgJson["username"]
    
    user = User.query.filter(
        User.username==username).first()
    if user is None: 
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"]=user.id

    return jsonify({
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "city": user.city,
        "internal_number": user.internal_number,
        "birth_year": user.birth_year,
        "card_number": user.card_number,
        "apartment_ID": user.apartment_ID
    })           
       

@ login_blueprint.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    msgJson = request.get_json()
    name = msgJson["name"]
    surname = msgJson["surname"]
    password = msgJson["password"]
    city = msgJson["city"]
    username = msgJson["username"]
    birth_year = msgJson["birth_year"]
    card_number = msgJson["card_number"]
    apartment_ID = msgJson["apartment_ID"]
    internal_number = msgJson["internal_number"]
    existing_user_username = User.query.filter(
            User.username==username).first() is not None
    if existing_user_username: 
            return jsonify({"error": "Username already exists"}), 409
    
    new_user = User(
            Person(
                username=username,
                name=name,
                surname=surname,
                password=generate_password(password), 
                city=city,
                birth_year=birth_year,
                card_number=card_number
            ),
            apartment_ID,
            internal_number,
        )
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id


    return jsonify({
        "id": new_user.id,
        "name": new_user.name,
        "surname": new_user.surname,
        "city": new_user.city,
        "internal_number": new_user.internal_number,
        "birth_year": new_user.birth_year,
        "card_number": new_user.card_number,
        "apartment_ID": new_user.apartment_ID
    })


#OPERATOR

@ login_blueprint.route('/registeroperator', methods=['GET', 'POST'])
def registeroperator():
    msgJson = request.get_json()
    name = msgJson["name"]
    surname = msgJson["surname"]
    password = msgJson["password"]
    city = msgJson["city"]
    username = msgJson["username"]
    birth_year = msgJson["birth_year"]
    card_number = msgJson["card_number"]
    id_operator = msgJson["id_operator"]
    existing_operator_username = Operator.query.filter(
            Operator.username==username).first() is not None
    if existing_operator_username: 
        return jsonify({"error": "Username already exists"}), 409
    
    new_user = Operator(
            Person(
                username=username,
                name=name,
                surname=surname,
                password=generate_password(password), 
                city=city,
                birth_year=birth_year,
                card_number=card_number
            ),
            id_operator,
        )
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id

    return jsonify({
            "id": new_user.id,
            "name": new_user.name,
            "surname": new_user.surname,
            "city": new_user.city,
            "birth_year": new_user.birth_year,
            "card_number": new_user.card_number,
            "id_operator": new_user.id_operator
    })

@login_blueprint.route('/loginoperator', methods=['GET', 'POST'])
def loginoperator():
    msgJson = request.get_json()
    password = msgJson["password"]
    username = msgJson["username"]
    
    operator = Operator.query.filter(
        Operator.username==username).first()
    if operator is None: 
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(operator.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"]=operator.id

    return jsonify({
            "id": operator.id,
            "name": operator.name,
            "surname": operator.surname,
            "city": operator.city,
            "birth_year": operator.birth_year,
            "card_number": operator.card_number,
            "id_operator": operator.id_operator
    })       


#ADMIN

@login_blueprint.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    msgJson = request.get_json()
    password = msgJson["password"]
    username = msgJson["username"]
    
    user = Admin.query.filter(
        Admin.username==username).first()
    if user is None: 
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"]=user.id

    return jsonify({
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "city": user.city,
        "birth_year": user.birth_year,
        "card_number": user.card_number,
    })           
       

@ login_blueprint.route('/registeradmin', methods=['GET', 'POST'])
def registeradmin():
    msgJson = request.get_json()
    name = msgJson["name"]
    surname = msgJson["surname"]
    password = msgJson["password"]
    city = msgJson["city"]
    username = msgJson["username"]
    birth_year = msgJson["birth_year"]
    card_number = msgJson["card_number"]
    
    existing_admin_username = Admin.query.filter(
            Admin.username==username).first() is not None
    if existing_admin_username: 
            return jsonify({"error": "Username already exists"}), 409
    
    new_user = Admin(
            Person(
                username=username,
                name=name,
                surname=surname,
                password=generate_password(password), 
                city=city,
                birth_year=birth_year,
                card_number=card_number
            )
        )
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id


    return jsonify({
        "id": new_user.id,
        "name": new_user.name,
        "surname": new_user.surname,
        "city": new_user.city,
        "birth_year": new_user.birth_year,
        "card_number": new_user.card_number,
    })

def generate_password(password):
    return bcrypt.generate_password_hash(password, 10).decode('utf-8')

def checkpassword(hash_password, password):
    bcrypt.check_password_hash(hash_password, password)