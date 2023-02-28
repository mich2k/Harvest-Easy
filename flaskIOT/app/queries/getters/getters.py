from app.database.tables import Admin, Apartment, Bin, User, UserTG, LeaderBoard, BinRecord
from flask import Blueprint
from app.utils.utils import Utils
from flask_jwt_extended import jwt_required
from app.database.__init__ import db
from flask import jsonify

get_blueprint = Blueprint("getters", __name__, template_folder="templates", url_prefix="/get")

@get_blueprint.route('/prevision/<int:id_bin>')
@jwt_required()
def getprevision(id_bin):
    bin = Bin.query.filter(Bin.id_bin == id_bin).first()
    return jsonify(bin.previsione_status)


@get_blueprint.route("/getprofileuser/<string:uid>", methods=["GET"])
@jwt_required()
def getprofileuser(uid):
    user = User.query.filter(User.username==uid).first()
    apartment_user= Apartment.query.filter(Apartment.apartment_name==user.apartment_ID).first()
    bins=Bin.query.filter(Bin.apartment_ID==user.apartment_ID).all()
  
    bidoni_user=[]
    for bin in bins:
        ultimo_bin_record = (
            BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        )
        dict={
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
        "n_internals":apartment_user.n_internals,
        "associated_admin": apartment_user.associated_admin,
        "bins":bidoni_user
   })

@get_blueprint.route("/dataAdmin/<string:uid>", methods=["GET"])
@jwt_required()
def dataAdmin(uid):
    res = Admin.query.where(Admin.username == uid).all()

    return Utils.sa_dic2json(res)

# Getters for SuperUsers, return json

# Get: TUTTI I BIN DI UNA CITTÁ


@get_blueprint.route("/getBins/<string:city>", methods=["GET"])
def getbins(city):

    # Subquery: Tutti gli appartamenti della cittá indicata
    db.session.query()
    sq = db.session.query(Apartment.apartment_name).where(
        Apartment.city == city)

    # Query: Tutti i bin negli appartamenti selezionati
    res = Bin.query().filter(Bin.apartment_ID.in_(sq)).all()

    return Utils.sa_dic2json(res)


# Get: TUTTI GLI UTENTI DI UNA CITTÁ


@get_blueprint.route("/getUsers/<string:city>", methods=["GET"])
def getusers(city):

    # Subquery: Tutti gli appartamenti della cittá indicata
    sq = db.session.query(Apartment.apartment_name).where(
        Apartment.city == city)

    # Query: Tutti gli user negli appartamenti selezionati
    res = db.session.query(User).filter(User.apartment_ID.in_(sq)).all()

    return Utils.sa_dic2json(res)


# Get: tutti i tipi di bidone nell'appartamento indicato


@get_blueprint.route("/getypes/<string:apartment>", methods=["GET"])
def getypes(apartment):

    res = db.session.query(Bin.tipologia).filter(
        Bin.apartment_ID == apartment).all()

    return Utils.sa_dic2json(res)


# Get: user dell'appartamento indicato


@get_blueprint.route("/getApartmentUsers/<string:apartment>", methods=["GET"])
def getapartmentusers(apartment):

    res = db.session.query(User).filter(User.apartment_ID == apartment).all()

    return Utils.sa_dic2json(res)


# Get: tutte le info associate al bidone indicato


@get_blueprint.route("/getBinInfo/<string:idbin>", methods=["GET"])
def getbininfo(idbin):

    res = db.session.query(Bin).where(Bin.id_bin == idbin).all()

    return Utils.sa_dic2json(res)


@get_blueprint.route("/getrecord/<string:idbin>", methods=["GET"])
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


@get_blueprint.route("/getApartment/<string:name>", methods=["GET"])
def getapartment(name):
    res = db.session.query(Apartment).where(
        Apartment.apartment_name == name).all()

    return Utils.sa_dic2json(res)


# Get: ottengo lo score di un utente

@get_blueprint.route("/getScore/<string:usr>", methods=["GET"])
def getscore(usr):
    user = db.session.query(UserTG.associated_user).where(UserTG.id_user == usr).first()[0]
    
    if user is None:
        return Utils.get_response(400, 'User not found')
    
    res = LeaderBoard.query.where(LeaderBoard.associated_user == user).order_by(LeaderBoard.record_id.desc()).first()
    
    if res is None:
        return Utils.get_response(400, 'None')
        
    return Utils.get_response(200, str(res.score))


# Get: ottengo la sessione dell'utente


@get_blueprint.route("/getSession/<string:usr>", methods=["GET"])
def getsession(usr):

    if (
        db.session.query(UserTG)
        .where(UserTG.id_user == usr)
        .all()
    ):
        return Utils.get_response(200, str(True))

    return Utils.get_response(200, str(False))
