from flask import Blueprint, request, redirect, session
from sqlalchemy.exc import OperationalError
from app.utils.utils import Utils
from os import getenv

handler_blueprint = Blueprint("error", __name__)


@handler_blueprint.app_errorhandler(OperationalError)
def db_handler(error):

    # Il path che ha generato l'eccezione viene inserito all'interno del dizionario relativo alla sessione
    session["last_url"] = request.url

    print(f"WARNING! An error occured in: {request.url}\n" + str(error))
    
    if getenv('FLASK_CONFIG') == 'docker_local':
        return redirect("http://127.0.0.1:5000/db")

    
    return redirect("https://flask.gmichele.it/db")


@handler_blueprint.app_errorhandler(Exception)
def handler(error):
    
    return Utils.get_response(400, f"WARNING! An error occured in: {request.url} " + str(error))
