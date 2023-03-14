from flask import request, Blueprint, jsonify, session
from os import getenv
from app.database.tables import *
from app.database.__init__ import db
from ..utils.utils import Utils
from app.login.__init__ import bcrypt
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required
from datetime import timedelta
import requests
import json
from flasgger import swag_from

login_blueprint = Blueprint(
    "login", __name__, template_folder="templates", url_prefix="/login"
)


@login_blueprint.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@login_blueprint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

# USER


@login_blueprint.route('/loginuser', methods=['POST'])
@swag_from('docs/loginuser.yml')
def loginuser():
    msgJson = request.get_json()
    password = msgJson["password"]
    username = msgJson["username"]

    if password is None or username is None:
        return jsonify({"error": "Wrong email or password"}), 400

    user = User.query.filter(
        User.username == username).first()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    access_token = create_access_token(identity=username)
    print(session)
    return jsonify({
        "access_token": access_token,
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "city": user.city,
        "internal_number": user.internal_number,
        "birth_year": user.birth_year,
        "card_number": user.card_number,
        "apartment_ID": user.apartment_ID
    }), 200


@login_blueprint.route('/profileuser')
@jwt_required()
def profileuser():
    return jsonify({
        "about": "Hello! This is a user's profile"
    }), 200


@login_blueprint.route('/ApartmentInit', methods=['POST'])
@jwt_required()
# @swag_from('docs/registeruser.yml')
def registeruser():
    data = request.get_json()

    URL = getenv('URL_REVERSE')

    user = []
    user_tg = []
    bin = []

    # print(data)

    # Adding people
    for msgJson in data['final_people']:

        username = msgJson['name'] + msgJson['surname']

        if not username.isalnum() or " " in username:
            continue
            # return jsonify({'error': "Username should be alphanumeric, also no spaces"}), 400

        if db.session.query(User).where(
                User.username == username).first() is not None:
            continue
            # return jsonify({"error": "Username already exists"}), 409

        user.append(User(
            Person(
                username=username,
                name=msgJson["name"],
                surname=msgJson["surname"],
                password=generate_password(msgJson["password"]) ,
                city=data["common_city"],
                birth_year=msgJson["birth_year"],
                card_number=msgJson["rfid_card"]
            ),
            apartment_ID=data['apartment_name'],
            internal_number=msgJson["intern_number"],
        ))

        user_tg.append(UserTG(
            id_user=msgJson['telegramUsername'], id_chat="", logged=False, associated_user=username))

    # Adding bins
    for bins in data['apartment_waste_sorting']:
        bin.append(Bin(tipologia=bins, apartment_ID=data['apartment_name']))

    # https://osm.gmichele.it/reverse?lat=44.6280877&lon=10.9166076&format=json

    req = requests.get(
        URL + f"?lat={data['apartment_coords']['lat']}&lon={data['apartment_coords']['lon']}&format=json").json()

    apartment = Apartment(
        apartment_name=data["apartment_name"],
        city=req["address"]['city'],
        street=req["address"]["road"],
        lat=data['apartment_coords']['lat'],
        lng=data['apartment_coords']['lon'],
        apartment_street_number=req['address']['house_number'] if 'house_number' in req['address'] else "0",
        n_internals=len(user),
        associated_admin=data["admin_username"],
    )

    print(user, user_tg, bin)
    
    db.session.add(apartment)
    db.session.add_all(user)
    db.session.add_all(user_tg)
    db.session.add_all(bin)
    db.session.commit()

    return {"success": True}, 200

# OPERATOR


@ login_blueprint.route('/registeroperator', methods=['POST'])
# @swag_from('docs/registeroperator.yml')
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

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), 401

    if Operator.query.filter(
            Operator.username == username).first() is not None:
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

    access_token = create_access_token(identity=username)

    return jsonify({
        "access_token": access_token,
        "id": new_user.id,
        "name": new_user.name,
        "surname": new_user.surname,
        "city": new_user.city,
        "birth_year": new_user.birth_year,
        "card_number": new_user.card_number,
        "id_operator": new_user.id_operator
    }), 200


@login_blueprint.route('/loginoperator', methods=['POST'])
@swag_from('docs/loginoperator.yml')
def loginoperator():
    msgJson = request.get_json()
    password = msgJson["password"]
    username = msgJson["username"]

    if password is None or username is None:
        return jsonify({"error": "Wrong email or password"}), 400

    operator = Operator.query.filter(
        Operator.username == username).first()

    if operator is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(operator.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({
        "access_token": access_token,
        "id": operator.id,
        "name": operator.name,
        "surname": operator.surname,
        "city": operator.city,
        "birth_year": operator.birth_year,
        "card_number": operator.card_number,
        "id_operator": operator.id_operator
    }), 200


@login_blueprint.route('/profileoperator/<string:username>', methods=["GET"])
@jwt_required()
def profileoperator(username):
    if username is None:
        return jsonify({"error": "Username is not correct"}), 401

    operator = Operator.query.filter(
        Operator.username == username).first()

    if operator is None:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"msg": "Hello! Welcome %s in your profile" % (operator.name)}), 200

# ADMIN


@login_blueprint.route('/loginadmin', methods=['POST'])
@swag_from('docs/loginadmin.yml')
def loginadmin():
    msgJson = request.get_json()
    password = msgJson["password"]
    username = msgJson["username"]

    if password is None or username is None:
        return jsonify({"error": "Wrong email or password"}), 400

    user = Admin.query.filter(
        Admin.username == username).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({
        "access_token": access_token,
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "city": user.city,
        "birth_year": user.birth_year,
        "card_number": user.card_number,
    }), 200


@ login_blueprint.route('/registeradmin', methods=['POST'])
# @swag_from('docs/registeradmin.yml')
def registeradmin():
    msgJson = request.get_json()
    name = msgJson["name"]
    surname = msgJson["surname"]
    password = msgJson["password"]
    city = msgJson["city"]
    username = msgJson["username"]
    birth_year = msgJson["birth_year"]
    card_number = msgJson["card_number"]

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), 401

    if Admin.query.filter(
            Admin.username == username).first() is not None:
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

    access_token = create_access_token(identity=username)

    return jsonify({
        "access_token": access_token,
        "id": new_user.id,
        "name": new_user.name,
        "surname": new_user.surname,
        "city": new_user.city,
        "birth_year": new_user.birth_year,
        "card_number": new_user.card_number,
    }), 200


@login_blueprint.route('/profileadmin')
@jwt_required()
def profileadmin():
    return jsonify({
        "about": "Hello! This is an admin's profile"
    }), 200


def generate_password(password):
    return bcrypt.generate_password_hash(password, 10).decode('utf-8')


def checkpassword(hash_password, password):
    return bcrypt.check_password_hash(hash_password, password)
