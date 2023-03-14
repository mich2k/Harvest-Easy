import app.trap.trap as tp
from sqlalchemy import update, delete
from flask import request, Blueprint, session, redirect, jsonify
from app.database.tables import *
from .faker import create_faker
from .__init__ import db, DB_status
from ..utils.utils import Utils
from flask_jwt_extended import jwt_required

# Lo userò per verificare se il DB è stato già creato
db_manager = DB_status()

database_blueprint = Blueprint(
    "database", __name__, template_folder="templates", url_prefix="/db")

# CREA IL DB A RUNTIME, SE GIà PRESENTE DROPPA TUTTE LE TABLES
# È LA PRIMA ROUTE DA RAGGIUNGERE QUANDO SI AVVIA IL SISTEMA


@database_blueprint.route("/")
def createDB():
    """
    Verifico che il database non sia stato già istanziato
    Questo eviterà di perdere i nuovi record
    """

    if not db_manager.already_done:
        try:
            db.drop_all()
            db.create_all()

            # if getenv("FAKER") == "True":
            create_faker(db)
        except Exception as e:

            print('Error during db creation: ' + str(e))
        db_manager.setstatus(db, True)

        """
        Nel caso si fosse arrivati alla route /db per redirect
        allora sarà necessario ritornare alla route precedente
        quindi si farà un redirect ad essa
        """
        if "last_url" in session:
            print('last_url: ' + str(session['last_url']))
            return redirect(session["last_url"])

        return Utils.get_response(200, "Done")

    return Utils.get_response(500, "Already done")

# AGGIUNTA DI INFORMAZIONI SUL BIDONE
# Le informazioni saranno inviate mediante JSON ogni N secondi.


@database_blueprint.route("/addrecord", methods=["POST"])
def addrecord():
    msgJson = request.get_json()
<<<<<<< HEAD

=======
    
>>>>>>> parent of 3ae3efc3 (Merge branch 'main' of)
    msgJson["status"] = Utils.calcolastatus(
        Utils,
        msgJson["id_bin"],
        msgJson["riempimento"],
        msgJson["roll"],
        msgJson["pitch"],
        msgJson["co2"],
        False
    )
    msgJson["timestamp"] = str(datetime.utcnow().replace(microsecond=0))
    sf = BinRecord(msgJson)
    db.session.add(sf)
    db.session.commit()

    return "Done", 200

# Adders

# AGGIUNTA DI UN APARTMENT
# inserire qui lat e long dell'appartamento tramite chiamata ad API
# da verificare chiamata ad API

# Print tables


@database_blueprint.route('/getrecord/<string:idbin>')
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


@database_blueprint.route("/items", methods=["GET"])
def stampaitems():
    res = []
    elenco = [
        Bin.query.order_by(Bin.id_bin.desc()).all(),
        Apartment.query.order_by(Apartment.apartment_name.desc()).all(),
        User.query.order_by(User.username.desc()).all(),
        Admin.query.order_by(Admin.username.desc()).all(),
        BinRecord.query.order_by(BinRecord.id_record.desc()).all(),
        UserTG.query.all(),
    ]

    for queries in elenco:
        res.append({queries[0].__tablename__: Utils.sa_dic2json(queries)})

    return res


@database_blueprint.route("/records")
def printmore():
    res = []

    elenco = [AlterationRecord.query.all(),
              LeaderBoard.query.all()]

    for queries in elenco:
        res.append({queries[0].__tablename__: Utils.sa_dic2json(queries)})

    return res

# delete


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

    bin_records = BinRecord.query.filter(BinRecord.associated_bin == id_bin)
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
    bins = Bin.query.filter(Bin.apartment_ID == apartment_name)
    for bin in bins:
        bin_records = BinRecord.query.filter(
            BinRecord.associated_bin == bin.id_bin)
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

# Route sfruttate dal bot telegram

# solved e report sono route utilizzate per comunicare se un evento di vandalismo sia stato risolto o meno
# solved si occupa di aggiornare la leaderboard


@database_blueprint.route('/solved/<string:uid>&<string:idbin>')
def solved(uid, idbin):
    """
        Workflow:
        - 1): Dall'uid ottengo l'utente
        - 2): Dall'idbin ottengo l'alteration record attiva
        - 2): Aggiorno il campo is_solved
        - 3): Controllo se un utente è inserito nella Leaderboard mediante lo score
            - 3.1): Se si aggiorno il punteggio (score non None)
            - 3.2): Altrimenti lo aggiungo e aggiorno il punteggio (score None)    
    """

    user = db.session.query(UserTG.associated_user).where(
        UserTG.id_chat == uid).first()[0]
    record = db.session.query(AlterationRecord.alteration_id).filter(
        AlterationRecord.associated_bin == idbin).where(AlterationRecord.is_solved == False).first()[0]

    # Check if already solved
    if not record:
        return Utils.get_response(200, 'Segnalazione già risolta')

    last_score = LeaderBoard.query.where(LeaderBoard.associated_user == user).order_by(
        LeaderBoard.record_id.desc()).first()

    db.session.add(LeaderBoard(last_score.score +
                   10 if last_score else 10, idbin, user, record))
    db.session.commit()

    return Utils.get_response(200, 'Fatto, aggiunti 10 punti per la segnalazione')


@database_blueprint.route('/report/<string:uid>&<string:idbin>')
def report(uid, idbin):
    db.session.execute(
        update(AlterationRecord)
        .where(AlterationRecord.associated_bin == idbin)
        .values({"is_solved": True})
    )
    return Utils.get_response(200, f'Contacting HERA from {uid} for {idbin}')


# ONLY FOR TESTING PURPOSES


@database_blueprint.route("/testrap")
def test_trap():
    tp.report(1, db, filling=56)
    tp.report(2, db, coord=56)
    tp.report(6, db, filling=56)
    tp.report(7, db, coord=56)
    tp.report(3, db, filling=56, coord=56, co2=56)

    return 'Done'


@database_blueprint.route("/testleaderboard/<string:user>&<string:idbin>")
def test_leaderboard(user, idbin):
    try:
        record = db.session.query(AlterationRecord.alteration_id).filter(
            AlterationRecord.associated_bin == idbin).where(AlterationRecord.is_solved == False).first()[0]

        # Check if already solved
        if not record:
            return Utils.get_response(200, 'Segnalazione già risolta')
        last_score = LeaderBoard.query.where(LeaderBoard.associated_user == user).order_by(
            LeaderBoard.record_id.desc()).first()

        db.session.add(LeaderBoard(last_score.score +
                       10 if last_score else 10, idbin, user, record))
        db.session.commit()
    except:
        return 'Error'
    return 'Done'
