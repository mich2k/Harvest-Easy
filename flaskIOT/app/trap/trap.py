from flask import Blueprint, request
from app.database.tables import Apartment, BinRecord, Bin
from app.database.__init__ import db
import json
import datetime
import requests
from sqlalchemy.sql.expression import func
from os import getenv

WEATHER_API_KEY = getenv('WHEATHER_KEY')
trap_blueprint = Blueprint('trap', __name__)
#Ricevo il dato, ottengo l'id e modifico lo status


@trap_blueprint.route('/full')
def change_status_f():
    msgJson = request.get_json()
    BinRecord.query()
    


@trap_blueprint.route('/rigged')
def change_status_r():
    msgJson = request.get_json()

@trap_blueprint.route('/getstatus')
def calcolastatus():
    # 1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    soglie={"plastica": 0.9, "carta": 0.9, "vetro": 0.8, "umido": 0.7} #soglie fisse
    #soglia_umido={"primavera": 0.6, "estate": 0.5, "autunno": 0.7, "inverno": 0.9} #soglia dinamica per l'organico in base alla stagione
    dd_umido={"medie": 5, "alte": 3, "altissime": 2} #soglia dinamica per l'organico in base alla temperatura

    status_attuale=1 #-->quando non ci sono istanze nella tabella
    tipologia = (Bin.query.filter_by(Bin.id_bin == msgJson["id_bin"]))[0].tipologia
    soglia_attuale=0
    if (tipologia=='umido'):
        now = datetime.datetime.now()
        mese=now.month
        giorno=now.day
        if(mese>=4 and mese<=10): #mesi caldi
            apartment_ID=(Bin.query.filter_by(Bin.id_bin == msgJson["id_bin"]))[0].apartment_ID
            lat=(Apartment.query.filter_by(Apartment.apartment_name==apartment_ID))[0].lat
            lon=(Apartment.query.filter_by(Apartment.apartment_name==apartment_ID))[0].lng
            WEATHERE_API_URL = f'GET https://api.openweathermap.org/data/2.5/weather'
            params = {
                'lat':lat,
                'lon':lon,
                'appid': WEATHER_API_KEY
            }
            req = requests.get(WEATHERE_API_URL, params=params)
            res = req.json()
            temp = res['object'][0]['main']['temp']-272,15 #conversione kelvin-celsius
            dd_time=0
            if(temp>=20 and temp<=25): #medie
                dd_time=dd_umido["media"]
            if(temp>25 and temp<=30): #alte
                dd_time=dd_umido["alte"]
            if(temp>30): #altissime
                dd_time=dd_umido["altissime"]
            #controllo che umido venga svuotato ogni quattro giorni
            timestamp=BinRecord.query(func.min(BinRecord.timestamp)).filter_by(BinRecord.id_bin==msg["id_bin"] and (BinRecord.status==1 or BinRecord.status==4))
            last_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
            if((now-last_date).day>dd_time): 
                soglia_attuale=0
        else:
            soglia_attuale=soglie["umido"]
    elif(tipologia=='plastica'):
        soglia_attuale=soglie["plastica"]
    elif(tipologia=='carta'):
        soglia_attuale=soglie["carta"]
    elif(tipologia=='vetro'):
        soglia_attuale=soglie["vetro"]

    bin_attuale=BinRecord.query.all()
    if(len(bin_attuale)>0): 
        status_attuale=bin_attuale[0].status

    riempimento_attuale=msgJson['riempimento']


    if(status_attuale==1 and float(riempimento_attuale)>=soglia_attuale): status_attuale=2
    if(status_attuale==3 and float(riempimento_attuale)>=soglia_attuale): status_attuale=4
    if(status_attuale==2 and float(riempimento_attuale)<soglia_attuale): status_attuale=1
    if(status_attuale==4 and float(riempimento_attuale)<soglia_attuale): status_attuale=3
    return status_attuale

    