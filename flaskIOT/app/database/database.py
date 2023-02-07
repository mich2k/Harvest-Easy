import requests
from sqlalchemy import update, delete
from flask import request, Blueprint, session, redirect, jsonify
from os import getenv
from app.database.tables import *
from .faker import create_faker
from .__init__ import db, DB_status
from ..utils.utils import Utils
from app.login.login import checkpassword
from flask_jwt_extended import jwt_required

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
            print(session['last_url'])
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
@jwt_required() 
def addbin():
    msgJson = request.get_json()

    db.session.add(Bin(msgJson))
    db.session.commit()

    return Utils.get_response(200, "Done")


# TODO Creare un'unica route per l'aggiunta di un utente/admin/operatore sfruttando un campo: role

# AGGIUNTA DI UN USER


@database_blueprint.route("/adduser", methods=["POST"])
@jwt_required() 
def adduser():
    msgJson = request.get_json()

    user = User(
        Person(
            username=msgJson["username"],
            name=msgJson["name"],
            surname=msgJson["surname"],
            password=msgJson["password"],
            city=msgJson["city"],
            birth_year=msgJson["year"],
            card_number=msgJson["card_number"]
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
    methods=["GET"]
)
@jwt_required() 
def addadmin(uid, name, surname, password, city, birth_year):
    admin = Admin(Person(uid, name, surname, password, city, birth_year))

    db.session.add(admin)
    db.session.commit()

    return Utils.get_response(200, "Done")


# AGGIUNTA DI UN OPERATORE


@database_blueprint.route("/addoperator", methods=["POST"])
@jwt_required() 
def addoperator():
    msgJson = request.get_json()
    operator = Operator(
        Person(
            username=msgJson["username"],
            name=msgJson["name"],
            surname=msgJson["surname"],
            password=msgJson["password"],
            city=msgJson["city"],
            birth_year=msgJson["year"],
            card_number=msgJson["card_number"],
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
@jwt_required() 
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
            if uid == user.card_number:
                if status_attuale == 1:
                    return jsonify({"code": 200})
                else:
                    #cerco il bidone più vicino
                    return jsonify({"code": 201})
    
    if len(admins) > 0:
        for admin in admins:
            if uid == admin.uid:
                if status_attuale == 1:
                    return jsonify({"code": 200})
                else:
                    # cerco il bidone più vicino
                    return jsonify({"code": 201})
    
    if len(operators) > 0:
        for operator in operators:
            if uid == operator.card_number:
                return jsonify({"code": 203})

    return jsonify({"code": 202})


# Print tables
@database_blueprint.route("/items", methods=["GET"])
def stampaitems():
    res = []
    elenco = [
        Bin.query.order_by(Bin.id_bin.desc()).all(),
        Apartment.query.order_by(Apartment.apartment_name.desc()).all(),
        User.query.order_by(User.username.desc()).all(),
        Admin.query.order_by(Admin.uid.desc()).all(),
        BinRecord.query.order_by(BinRecord.id_record.desc()).all(),
        TelegramIDChatUser.query.all(),
    ]

    for queries in elenco:
        res.append({queries[0].__tablename__: Utils.sa_dic2json(queries)})

    return res

 
# Getters

@database_blueprint.route("/dataAdmin/<string:uid>", methods=["GET"])
@jwt_required() 
def dataAdmin(uid):
    res = Admin.query.where(Admin.uid == uid).all()

    return Utils.sa_dic2json(res)


@database_blueprint.route("/checkAdmin/<string:uid>&<string:password>", methods=["GET"])
def login(uid, password):

    access_allowed = False
    for asw in db.session.query(
        Admin.uid == uid and checkpassword(Admin.password, password)
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

@database_blueprint.route("/getrecord/<string:idbin>", methods=["GET"])
def getbinrecord(idbin):

    ultimo_bin_record = (
            BinRecord.query.filter(BinRecord.associated_bin == idbin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        )
    
    return {
        "status": ultimo_bin_record.status,
        "temperatura": ultimo_bin_record.temperature,
        "riempimento": ultimo_bin_record.riempimento
    }


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


#delete

@database_blueprint.route("/deleteuser/<string:username>", methods=["GET"])
def deleteuser(username):
    """
    elimino l'utente
    """
    if username is None:
        return jsonify({"Erroe": "Username is not correct"})
    
    db.session.execute(
        delete(User)
        .where(User.username == username)
    )
    db.session.commit()
    
    return jsonify({"msg": "User correctly deleted"}), 200


@database_blueprint.route("/deleteadmin/<string:username>", methods=["GET"])
def deleteadmin(username):
    """
    elimino l'admin
    """
    if username is None:
        return jsonify({"Erroe": "Username is not correct"})
    
    db.session.execute(
        delete(Admin)
        .where(Admin.username == username)
    )
    db.session.commit()
    
    return jsonify({"msg": "Admin correctly deleted"}), 200


@database_blueprint.route("/deleteoperator/<string:username>", methods=["GET"])
def deleteoperator(username):
    """
    elimino l'operatore
    """
    if username is None:
        return jsonify({"Erroe": "Username is not correct"})
    
    db.session.execute(
        delete(Operator)
        .where(Operator.username == username)
    )
    db.session.commit()
    
    return jsonify({"msg": "Operator correctly deleted"}), 200


@database_blueprint.route("/deletebin/<string:id_bin>", methods=["GET"])
def deletebin(id_bin):
    """
    elimino il bidone e i relativi record
    """
    if id_bin is None:
        return jsonify({"Erroe": "id_bin is not correct"})

    bin_records=BinRecord.query.filter(BinRecord.associated_bin==id_bin)
    for bin_record in bin_records:
        db.session.execute(
            delete(BinRecord)
            .where(BinRecord.id_record == bin_record.id_record)
        )
    db.session.commit()

    db.session.execute(
        delete(Bin)
        .where(Bin.id_bin == id_bin)
    )
    db.session.commit()
    
    return jsonify({"msg": "Bin correctly deleted"}), 200

@database_blueprint.route("/deleteapartment/<string:apartment_name>", methods=["GET"])
def deleteapartment(apartment_name):
    """
    elimino l'appartamento, i relativi bidoni e i relativi record
    """
    if apartment_name is None:
        return jsonify({"Erroe": "apartment_name is not correct"})
    bins = Bin.query.filter(Bin.apartment_ID==apartment_name)
    for bin in bins:
        bin_records=BinRecord.query.filter(BinRecord.associated_bin==bin.id_bin)
        for bin_record in bin_records:
            db.session.execute(
                delete(BinRecord)
                .where(BinRecord.id_record == bin_record.id_record)
            )
            db.session.commit()

        db.session.execute(
        delete(Bin)
        .where(Bin.id_bin == bin.id_bin)
        )
        db.session.commit()

    db.session.execute(
        delete(Apartment)
        .where(Apartment.apartment_name == apartment_name)
    )
    db.session.commit()
    
    return jsonify({"msg": "Apartment correctly deleted"}), 200

@database_blueprint.route("/deletebinrecord/<string:id_record>", methods=["GET"])
def deletebinrecord(id_record):
    """
    elimino il bin record
    """
    if id_record is None:
        return jsonify({"Erroe": "id_record is not correct"})
    
    db.session.execute(
        delete(BinRecord)
        .where(BinRecord.id_record == id_record)
    )
    db.session.commit()
    
    return jsonify({"msg": "BinRecord correctly deleted"}), 200
