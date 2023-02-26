from app.database.tables import User, Operator,Admin, BinRecord, UserTG
from app.utils.utils import Utils
from app.login.login import checkpassword
from app.database.__init__ import db
from flask import Blueprint
import json

check_blueprint = Blueprint("checkers", __name__, template_folder="templates", url_prefix="/check")


@check_blueprint.route("/checkuid/<string:uid>&<int:id_bin>", methods=["GET"])
def checkuid(uid, id_bin):

    users = User.query.all()
    operators = Operator.query.all()
    admins = Admin.query.all()
    ultimo_bin_record = (
        BinRecord.query.filter(BinRecord.associated_bin == id_bin)
        .order_by(BinRecord.timestamp.desc())
        .first()
    )

    status_attuale = None if ultimo_bin_record is None else ultimo_bin_record.status

    if len(users) > 0:
        for user in users:
            if uid == user.card_number:
                if status_attuale == 1:
                    return json.dump({"code": 200})
                else:
                    # cerco il bidone più vicino
                    return json.dump({"code": 201})

    if len(admins) > 0:
        for admin in admins:
            if uid == admin.uid:
                if status_attuale == 1:
                    return json.dump({"code": 200})
                else:
                    # cerco il bidone più vicino
                    return json.dump({"code": 201})

    if len(operators) > 0:
        for operator in operators:
            if uid == operator.card_number:
                return json.dump({"code": 203})

    return json.dump({"code": 202})


@check_blueprint.route("/checkAdmin/<string:uid>&<string:password>", methods=["GET"])
def checkadmin(uid, password):

    access_allowed = False
    
    for asw in db.session.query(Admin.password).where(Admin.username == uid).all():
        if asw[0]:
            print(asw)
            if checkpassword(asw[0], password):
                access_allowed = True

    return Utils.get_response(200 if access_allowed else 400, str(access_allowed))

@check_blueprint.route("/checkUsername/<string:usr>", methods=["GET"])
def checkusername(usr):
    found = False
    for asw in db.session.query(UserTG.id_user == usr).all():
        if asw[0]:
            found = True

    return Utils.get_response(200 if found else 400, str(found))


@check_blueprint.route("/checkSession/<string:userid>", methods=["GET"])
def checksession(userid):
    found = False
    for asw in db.session.query(UserTG.id_user == userid).all():
        if asw[0]:
            found = True

    return Utils.get_response(200 if found else 400, str(found))