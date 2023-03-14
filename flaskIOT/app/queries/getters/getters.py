from app.database.tables import Admin, Apartment, Bin, User, UserTG, LeaderBoard, BinRecord
from flask import Blueprint
from app.utils.utils import Utils
from app.database.__init__ import db
from flask import jsonify
from os import listdir, getenv
from os.path import isdir
from flask_jwt_extended import jwt_required
from app.utils.utils import Utils
from flasgger import swag_from
from datetime import datetime, timedelta
import requests
import base64

get_blueprint = Blueprint(
    "getters", __name__, template_folder="templates", url_prefix="/get")
URL = getenv('URL_get')


def getbinrecord(id_bin):

    ultimo_bin_record = (
        BinRecord.query.filter(BinRecord.associated_bin == id_bin)
        .order_by(BinRecord.timestamp.desc())
        .first()
    )

    return {
        "status": ultimo_bin_record.status,
        "temperatura": ultimo_bin_record.temperature,
        "riempimento": ultimo_bin_record.riempimento
    }


@get_blueprint.route('/prevision/<string:apartment>')
# @jwt_required()
def getprevision(apartment):

    bins = db.session.query(Bin.id_bin, Bin.previsione_status, Bin.tipologia).where(
        Bin.apartment_ID == apartment).all()

    answ = {}

    for bin in list(bins):

        data = {}
        resp = getbinrecord(bin[0])

            
        data['previsione_status'] = bin[1]
        data['tipologia'] = bin[2]
        data['status'] = resp['status']
        data['riempimento'] = resp['riempimento']

        answ[bin[2]] = data

    return jsonify(answ)


@get_blueprint.route("/getprofileuser/<string:uid>", methods=["GET"])
@jwt_required()
def getprofileuser(uid):
    user = User.query.filter(User.username == uid).first()
    if user is None:
        return jsonify({"errore": "username non corretto"})

    apartment_user = Apartment.query.filter(
        Apartment.apartment_name == user.apartment_ID).first()
    bins = Bin.query.filter(Bin.apartment_ID == user.apartment_ID).all()

    bidoni_user = []
    for bin in bins:
        ultimo_bin_record = (
            BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        )
        dict = {
            "id_bin": bin.id_bin,
            "tipologia": bin.tipologia,
            "previsione_status": bin.previsione_status,
            "ultimo_svuotamento": bin.ultimo_svuotamento,
            "status": ultimo_bin_record.status
        }
        bidoni_user.append(dict)

    return jsonify({
        "username": uid,
        "name": user.name,
        "surname": user.username,
        "user_city": user.city,
        "birth_year": user.birth_year,
        "card_number": user.card_number,
        "internal_number": user.internal_number,
        "apartment_name": user.apartment_ID,
        "apartment_city": apartment_user.city,
        "street": apartment_user.street,
        "apartment_street_number": apartment_user.apartment_street_number,
        "n_internals": apartment_user.n_internals,
        "associated_admin": apartment_user.associated_admin,
        "bins": bidoni_user
    })


@get_blueprint.route("/getprofileadmin/<string:uid>", methods=["GET"])
@jwt_required()
def getprofileadmin(uid):
    admin = Admin.query.filter(Admin.username == uid).first()
    if admin is None:
        return jsonify({"errore": "username non corretto"})

    apartments = Apartment.query.filter(
        Apartment.associated_admin == uid).all()
    appartment_list = []
    for apartment in apartments:
        dictap = {
            "apartment_name": apartment.apartment_name,
            "apartment_city": apartment.city,
            "street": apartment.street,
            "apartment_street_number": apartment.apartment_street_number,
            "n_internals": apartment.n_internals,
            "bins": None
        }

        bins = Bin.query.filter(
            Bin.apartment_ID == apartment.apartment_name).all()
        bidoni = []
        for bin in bins:
            ultimo_bin_record = (
                BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
                .order_by(BinRecord.timestamp.desc())
                .first()
            )
            dict = {
                "id_bin": bin.id_bin,
                "tipologia": bin.tipologia,
                "previsione_status": bin.previsione_status,
                "ultimo_svuotamento": bin.ultimo_svuotamento,
                "status": Utils.getstringstatus(ultimo_bin_record.status),
                "temperature": ultimo_bin_record.temperature,
                "humidity": ultimo_bin_record.humidity,
                "riempimento": ultimo_bin_record.riempimento
            }
            bidoni.append(dict)
        dictap["bins"] = bidoni
        appartment_list.append(dictap)

    return jsonify({
        "username": uid,
        "name": admin.name,
        "surname": admin.username,
        "user_city": admin.city,
        "birth_year": admin.birth_year,
        "card_number": admin.card_number,
        "apartments": appartment_list,
    })


@get_blueprint.route("/dataAdmin/<string:uid>", methods=["GET"])
@jwt_required()
def dataAdmin(uid):
    res = Admin.query.where(Admin.username == uid).all()

    return Utils.sa_dic2json(res)

# Getters for SuperUsers, return json

# Get: TUTTI I BIN DI UNA CITTÁ


@get_blueprint.route("/getBins/<string:city>", methods=["GET"])
@swag_from('docs/getBins.yml')
def getbins(city):
    # Subquery: Tutti gli appartamenti della cittá indicata
    sq = db.session.query(Apartment.apartment_name).where(
        Apartment.city == city)

    # Query: Tutti gli user negli appartamenti selezionati
    res = db.session.query(Bin).filter(Bin.apartment_ID.in_(sq)).all()
    return Utils.sa_dic2json(res)


# Get: TUTTI GLI UTENTI DI UNA CITTÁ


@get_blueprint.route("/getUsers/<string:city>", methods=["GET"])
@swag_from('docs/getUsers.yml')
def getusers(city):

    # Subquery: Tutti gli appartamenti della cittá indicata
    sq = db.session.query(Apartment.apartment_name).where(
        Apartment.city == city)

    # Query: Tutti gli user negli appartamenti selezionati
    res = db.session.query(User).filter(User.apartment_ID.in_(sq)).all()

    return Utils.sa_dic2json(res)


# Get: tutti i tipi di bidone nell'appartamento indicato


@get_blueprint.route("/getypes/<string:apartment>", methods=["GET"])
@swag_from('docs/getypes.yml')
def getypes(apartment):
    res = db.session.query(Bin).filter(
        Bin.apartment_ID == apartment).all()
    tipologie = []
    for re in res:
        tipologie.append(re.tipologia)
    return jsonify(tipologie)


# Get: user dell'appartamento indicato


@get_blueprint.route("/getApartmentUsers/<string:apartment>", methods=["GET"])
@swag_from('docs/getapartment_users.yml')
def getapartmentusers(apartment):

    res = db.session.query(User).filter(User.apartment_ID == apartment).all()

    return Utils.sa_dic2json(res)


# Get: tutte le info associate al bidone indicato


@get_blueprint.route("/getBinInfo/<string:id_bin>", methods=["GET"])
@swag_from('docs/getBinInfo.yml')
def getbininfo(id_bin):

    res = db.session.query(Bin).where(Bin.id_bin == id_bin).all()

    return Utils.sa_dic2json(res)


# Get: ottengo tutte le informazioni dell'appartamento indicato


@get_blueprint.route("/getApartment/<string:name>", methods=["GET"])
@swag_from('docs/getApartment.yml')
def getapartment(name):
    res = db.session.query(Apartment).where(
        Apartment.apartment_name == name).all()

    return Utils.sa_dic2json(res)


# Get: ottengo lo score di un utente

@get_blueprint.route("/getScore/<string:usr>", methods=["GET"])
def getscore(usr):
    user = db.session.query(UserTG.associated_user).where(
        UserTG.id_user == usr).first()[0]

    if user is None:
        return Utils.get_response(400, 'User not found')

    res = LeaderBoard.query.where(LeaderBoard.associated_user == user).order_by(
        LeaderBoard.record_id.desc()).first()

    if res is None:
        return Utils.get_response(400, 0)

    return Utils.get_response(200, str(res.score), True)


# Get: ottengo la sessione dell'utente


@get_blueprint.route("/getSession/<string:usr>", methods=["GET"])
def getsession(usr):

    if (
        db.session.query(UserTG)
        .where(UserTG.id_user == usr)
        .all()
    ):
        return Utils.get_response(200, str(True), True)

    return Utils.get_response(200, str(False), True)


# Get: ottengo la top10 della classifica generale

@get_blueprint.route("/leaderboard", methods=['GET'])
def getleaderboard():

    records = db.session.query(LeaderBoard.associated_user, db.func.count(
        LeaderBoard.score)*10).group_by(LeaderBoard.associated_user).all()
    asw = ""

    if records is not None:
        for record in records:
            asw += record[0] + ': ' + str(record[1]) + '\n'

        return Utils.get_response(200, asw, text=True)
    else:
        return Utils.get_response(200, "Empty Leaderboard", text=True)


@get_blueprint.route("/urlprevision/<string:apartment>")
def geturlprevision(apartment):
    out = {}
    files = []
    types = []
    for dir in listdir(f'./predictions/{apartment}/'):
        if isdir(f'./predictions/{apartment}/{dir}'):
            types.append(dir)
            files += [f'./predictions/{apartment}/{dir}/' + file for file in listdir(
                f'./predictions/{apartment}/{dir}') if file == 'forecast.png']

    for file, type in zip(files, types):
        print(file)
        with open(file, 'rb') as img_file:
            out[type] = base64.b64encode(img_file.read()).decode('ascii')

    return jsonify(out)
