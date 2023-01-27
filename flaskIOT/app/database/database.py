import requests
from sqlalchemy import update
from flask import request, Blueprint, session, redirect, jsonify
from os import getenv
from app.database.tables import *
from .faker import create_faker
from .__init__ import db, DB_status
from ..utils.utils import Utils
#from flasky import bcrypt

URL = "https://osm.gmichele.it/search"

# Lo userò per verificare se il DB è stato già creato
db_manager = DB_status()

database_blueprint = Blueprint(
    "database", __name__, template_folder="templates", url_prefix="/db"
)

# CREA IL DB A RUNTIME, SE GIà PRESENTE DROPPA TUTTE LE TABLES
# È LA PRIMA ROUTE DA RAGGIUNGERE QUANDO SI AVVIA IL SISTEMA


@database_blueprint.route("/")
def createDB():
    """
    Verifico che il database non sia stato già istanziato
    Questo eviterà di perdere i nuovi record
    """

    if not db_manager.already_done:

        db.drop_all()
        db.create_all()

        #if getenv("FAKER") == "True":
        create_faker(db)

        db_manager.setstatus(db, True)

        """
        Nel caso si fosse arrivati alla route /db per redirect
        allora sarà necessario ritornare alla route precedente
        quindi si farà un redirect ad essa
        """
        if "last_url" in session:
            return redirect(session["last_url"])

        return Utils.get_response(200, "Done")

    return Utils.get_response(500, "Already done")


# AGGIUNTA DI INFORMAZIONI SUL BIDONE
# Le informazioni saranno inviate mediante JSON ogni N secondi.


@database_blueprint.route("/addrecord", methods=["POST"])
def addrecord():
    msgJson = request.get_json()
    msgJson["status"] = 1 
    """
    Utils.calcolastatus(
        db,
        msgJson["id_bin"],
        msgJson["riempimento"],
        msgJson["roll"],
        msgJson["pitch"],
        msgJson["co2"],
    )
    """
    sf = BinRecord(msgJson)
    db.session.add(sf)
    db.session.commit()

    return Utils.get_response(200, "Done")


# AGGIUNTA DI UN BIDONE


@database_blueprint.route("/addbin", methods=["POST"])
def addbin():
    msgJson = request.get_json()

    db.session.add(Bin(msgJson))
    db.session.commit()

    return Utils.get_response(200, "Done")


# TODO Creare un'unica route per l'aggiunta di un utente/admin/operatore sfruttando un campo: role

# AGGIUNTA DI UN USER


@database_blueprint.route("/adduser", methods=["POST"])
def adduser():
    msgJson = request.get_json()

    user = User(
        Person(
            uid=msgJson["uid"],
            name=msgJson["name"],
            surname=msgJson["surname"],
            password=msgJson["password"],
            city=msgJson["city"],
            birth_year=msgJson["year"],
        ),
        apartment_ID=msgJson["apartment_ID"],
        internal_number=msgJson["internal_number"],
    )

    db.session.add(user)
    db.session.commit()

    return Utils.get_response(200, "Done")


# AGGIUNTA DI UN ADMIN


@database_blueprint.route(
    "/addAdmin/<string:uid>&<string:name>&<string:surname>&<string:password>&<string:city>&<int:birth_year>",
    methods=["GET"],
)
def addadmin(uid, name, surname, password, city, birth_year):
    admin = Admin(Person(uid, name, surname, password, city, birth_year))

    db.session.add(admin)
    db.session.commit()

    return Utils.get_response(200, "Done")


# AGGIUNTA DI UN OPERATORE


@database_blueprint.route("/addoperator", methods=["POST"])
def addoperator():
    msgJson = request.get_json()
    operator = Operator(
        Person(
            uid=msgJson["uid"],
            name=msgJson["name"],
            surname=msgJson["surname"],
            password=msgJson["password"],
            city=msgJson["city"],
            birth_year=msgJson["year"],
        ),
        id=msgJson["id"],
    )

    db.session.add(operator)
    db.session.commit()
    return Utils.get_response(200, "Done")


# AGGIUNTA DI UN APARTMENT
# inserire qui lat e long dell'appartamento tramite chiamata ad API
# da verificare chiamata ad API


@database_blueprint.route("/addapartment", methods=["POST"])
def addapartment():

    msgJson = request.get_json()

    address = (
        msgJson["street"] + " " + str(msgJson["street_number"]) + " " + msgJson["city"]
    )

    params = {
        "q": address + " Italia",
    }

    req = requests.get(URL, params=params)
    result = req.json()

    lat = result[0]["lat"]
    lng = result[0]["lon"]

    apartment = Apartment(
        apartment_name=msgJson["apartment_name"],
        city=msgJson["city"],
        street=msgJson["street"],
        lat=lat,
        lng=lng,
        apartment_street_number=msgJson["street_number"],
        n_internals=msgJson["n_internals"],
        associated_admin=msgJson["associated_admin"],
    )

    db.session.add(apartment)

    db.session.commit()

    return Utils.get_response(200, "Done")


# ACCESSO DI UN UTENTE AL BIDONE


@database_blueprint.route("/checkuid/<string:uid>&<int:id_bin>", methods=["GET"])
def check(uid, id_bin):

    users = User.query.all()
    operators = Operator.query.all()
    admins = Admin.query.all()
    ultimo_bin_record = (
        BinRecord.query.filter(BinRecord.associated_bin == id_bin)
        .order_by(BinRecord.timestamp.desc())
        .first()
    )

    if ultimo_bin_record is None:
        status_attuale = None
    else:
        status_attuale = ultimo_bin_record.status

    if len(users) > 0:
        for user in users:
            if uid == user.uid:
                if status_attuale == 1:
                    return jsonify({"code": 200})
                else:
                    # cerco il bidone più vicino
                    return jsonify({"code": 201, "vicino": ""})

    if len(admins) > 0:
        for admin in admins:
            if uid == admin.uid:
                if status_attuale == 1:
                    return jsonify({"code": 200})
                else:
                    # cerco il bidone più vicino
                    return jsonify({"code": 201, "vicino": ""})

    if len(operators) > 0:
        for operator in operators:
            if uid == operator.uid:
                return jsonify({"code": 203})

    return jsonify({"code": 202})


# Print tables
@database_blueprint.route("/items", methods=["GET"])
def stampaitems():
    res = []
    elenco = [
        Bin.query.order_by(Bin.id_bin.desc()).all(),
        Apartment.query.order_by(Apartment.apartment_name.desc()).all(),
        User.query.order_by(User.uid.desc()).all(),
        Admin.query.order_by(Admin.uid.desc()).all(),
        BinRecord.query.order_by(BinRecord.id_record.desc()).all(),
        TelegramIDChatUser.query.all(),
    ]

    for queries in elenco:
        res.append({queries[0].__tablename__: Utils.sa_dic2json(queries)})

    return res


# Getters


@database_blueprint.route("/dataAdmin/<string:uid>", methods=["GET"])
def dataAdmin(uid):
    res = Admin.query.where(Admin.uid == uid).all()

    return Utils.sa_dic2json(res)


@database_blueprint.route("/checkAdmin/<string:uid>&<string:password>", methods=["GET"])
def login(uid, password):

    access_allowed = False
    for asw in db.session.query(
        #Admin.uid == uid and bcrypt.check_password_hash(Admin.password, password)
    ).all():
        if asw[0]:
            access_allowed = True

    return Utils.get_json(200, {"allowed": access_allowed})


@database_blueprint.route("/checkUsername/<string:usr>", methods=["GET"])
def checkusername(usr):
    found = False
    for asw in db.session.query(TelegramIDChatUser.id_user == usr).all():
        if asw[0]:
            found = True

    return Utils.get_json(200, {"found": found})


@database_blueprint.route("/checkSession/<string:userid>", methods=["GET"])
def checksession(userid):
    found = False
    for asw in db.session.query(TelegramIDChatUser.id_user == userid).all():
        if asw[0]:
            found = True

    return Utils.get_json(200, found)


@database_blueprint.route("/setelegramSession/<string:usr>", methods=["GET"])
def setsession(usr):
    db.session.execute(
        update(TelegramIDChatUser)
        .where(TelegramIDChatUser.id_user == usr)
        .values({"logged": True})
    )
    db.session.commit()

    return Utils.get_response(200, "Done")


# Getters for SuperUsers, return json

# Get: TUTTI I BIN DI UNA CITTÁ


@database_blueprint.route("/getBins/<string:city>", methods=["GET"])
def getbins(city):

    # Subquery: Tutti gli appartamenti della cittá indicata
    db.session.query()
    sq = db.session.query(Apartment.apartment_name).where(Apartment.city == city)

    # Query: Tutti i bin negli appartamenti selezionati
    res = Bin.query().filter(Bin.apartment_ID.in_(sq)).all()

    return Utils.sa_dic2json(res)


# Get: TUTTI GLI UTENTI DI UNA CITTÁ


@database_blueprint.route("/getUsers/<string:city>", methods=["GET"])
def getusers(city):

    # Subquery: Tutti gli appartamenti della cittá indicata
    sq = db.session.query(Apartment.apartment_name).where(Apartment.city == city)

    # Query: Tutti gli user negli appartamenti selezionati
    res = db.session.query(User).filter(User.apartment_ID.in_(sq)).all()

    return Utils.sa_dic2json(res)


# Get: tutti i tipi di bidone nell'appartamento indicato


@database_blueprint.route("/getypes/<string:apartment>", methods=["GET"])
def getypes(apartment):

    res = db.session.query(Bin.tipologia).filter(Bin.apartment_ID == apartment).all()

    return Utils.sa_dic2json(res)


# Get: user dell'appartamento indicato


@database_blueprint.route("/getApartmentUsers/<string:apartment>", methods=["GET"])
def getapartmentusers(apartment):

    res = db.session.query(User).filter(User.apartment_ID == apartment).all()

    return Utils.sa_dic2json(res)


# Get: tutte le info associate al bidone indicato


@database_blueprint.route("/getBinInfo/<string:idbin>", methods=["GET"])
def getbininfo(idbin):

    res = db.session.query(Bin).where(Bin.id_bin == idbin).all()

    return Utils.sa_dic2json(res)


# Get: ottengo tutte le informazioni dell'appartamento indicato


@database_blueprint.route("/getApartment/<string:name>", methods=["GET"])
def getapartment(name):

    res = db.session.query(Apartment).where(Apartment.apartment_name == name).all()

    return Utils.sa_dic2json(res)


# Get: ottengo lo score di un utente


@database_blueprint.route("/getScore/<string:usr>", methods=["GET"])
def getscore(usr):

    res = db.session.query(LeaderBoard).where(LeaderBoard.associated_user == usr).all()

    return Utils.sa_dic2json(res)


# Get: ottengo la sessione dell'utente


@database_blueprint.route("/getSession/<string:usr>", methods=["GET"])
def getsession(usr):

    if (
        db.session.query(TelegramIDChatUser)
        .where(TelegramIDChatUser.id_user == usr)
        .all()
    ):
        return Utils.get_response(200, str(True))

    return Utils.get_response(200, str(False))
