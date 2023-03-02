from app.database.tables import UserTG
from app.utils.utils import Utils
from app.database.__init__ import db
from sqlalchemy import update
from flask import Blueprint

set_blueprint = Blueprint("setters", __name__, template_folder="templates", url_prefix="/set")

@set_blueprint.route("/set_TelegramSession/<string:usr>&<int:idchat>", methods=["GET"])
def setsession(usr, idchat):
    db.session.execute(
        update(UserTG)
        .where(UserTG.id_user == usr)
        .values({"logged": True, "id_chat": str(idchat)})
    )
    db.session.commit()

    return Utils.get_response(200, "Done", True)