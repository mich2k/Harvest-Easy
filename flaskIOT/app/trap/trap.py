from flask import Blueprint, request
from app.database.tables import Apartment, BinRecord, Bin

from os import getenv

WEATHER_API_KEY = getenv('WEATHER_API_KEY')

trap_blueprint = Blueprint('trap', __name__)
#Ricevo il dato, ottengo l'id e modifico lo status

@trap_blueprint.route('/full')
def change_status_f():
    msgJson = request.get_json()
    BinRecord.query()

@trap_blueprint.route('/rigged')
def change_status_r():
    msgJson = request.get_json()
